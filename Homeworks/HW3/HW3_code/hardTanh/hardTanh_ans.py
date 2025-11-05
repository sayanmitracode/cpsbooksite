import torch
import torch.nn as nn


class BoundHardTanh(nn.Hardtanh):
    def __init__(self,inplace=False):
        super(BoundHardTanh, self).__init__(inplace)

    @staticmethod
    def convert(act_layer):
        r"""Convert a HardTanh layer to BoundHardTanh layer

        Args:
            act_layer (nn.HardTanh): The HardTanh layer object to be converted.

        Returns:
            l (BoundHardTanh): The converted layer object.
        """
        # TODO: Return the converted HardTanH
        l = BoundHardTanh(act_layer.inplace)
        return l
        #pass

    def boundpropogate(self, last_uA, last_lA, start_node=None):
        """
        Propagate upper and lower linear bounds through the HardTanh activation function
        based on pre-activation bounds.

        Args:
            last_uA (tensor): A (the coefficient matrix) that is bound-propagated to this layer
            (from the layers after this layer). It's exclusive for computing the upper bound.

            last_lA (tensor): A that is bound-propagated to this layer. It's exclusive for computing the lower bound.

            start_node (int): An integer indicating the start node of this bound propagation

        Returns:
            uA (tensor): The new A for computing the upper bound after taking this layer into account.

            ubias (tensor): The bias (for upper bound) produced by this layer.

            lA( tensor): The new A for computing the lower bound after taking this layer into account.

            lbias (tensor): The bias (for lower bound) produced by this layer.

        """
        # These are preactivation bounds that will be used for form the linear relaxation.
        preact_lb = self.lower_l.clamp(max=1)
        preact_ub = self.upper_u.clamp(min=-1)
        # avoid division by 0 when both lb_r and ub_r are 0
        preact_ub = torch.max(preact_ub, preact_lb + 1e-8)

        lb_r = self.lower_l.clamp(min=-1).clamp(max=1)
        ub_r = self.upper_u.clamp(min=-1).clamp(max=1)

        
        # CROWN upper and lower linear bounds
        upper_d = (ub_r-lb_r) / (preact_ub-preact_lb)  # slope
        upper_b = (1- upper_d)*ub_r # intercept
        upper_d = upper_d.unsqueeze(1)

        lower_d = (ub_r-lb_r) / (preact_ub-preact_lb)  # slope
        lower_b = (1- lower_d)*lb_r # intercept
        lower_d = lower_d.unsqueeze(1)

        uA = lA = None
        ubias = lbias = 0

        if last_uA is not None:
            pos_uA = last_uA.clamp(min=0)
            neg_uA = last_uA.clamp(max=0)
            # Choose upper or lower bounds based on the sign of last_A
            # New linear bound coefficent.
            uA = upper_d * pos_uA + lower_d * neg_uA
            # New bias term. Adjust shapes to use matmul (better way is to use einsum).
            mult_uA_1 = pos_uA.view(last_uA.size(0), last_uA.size(1), -1)
            ubias_1 = mult_uA_1.matmul(upper_b.view(upper_b.size(0), -1, 1))
            mult_uA_2 = neg_uA.view(last_uA.size(0), last_uA.size(1), -1)
            ubias_2 = mult_uA_2.matmul(lower_b.view(lower_b.size(0), -1, 1))
            ubias=(ubias_1+ubias_2).squeeze(-1)
        if last_lA is not None:
            pos_lA = last_lA.clamp(min=0)
            neg_lA = last_lA.clamp(max=0)
            # Choose upper or lower bounds based on the sign of last_A
            # New linear bound coefficent.
            lA = upper_d * neg_lA + lower_d * pos_lA
            # New bias term. Adjust shapes to use matmul (better way is to use einsum).
            mult_lA_1 = pos_lA.view(last_lA.size(0), last_lA.size(1), -1)
            lbias_1 = mult_lA_1.matmul(lower_b.view(lower_b.size(0), -1, 1))
            mult_lA_2 = neg_lA.view(last_lA.size(0), last_lA.size(1), -1)
            lbias_2 = mult_lA_2.matmul(upper_b.view(upper_b.size(0), -1, 1))
            lbias=(lbias_1+lbias_2).squeeze(-1)
   
        """
         Hints: 
         1. Have a look at the section 3.2 of the CROWN paper [1] (Case Studies) as to how segments are made for multiple activation functions
         2. Look at the HardTanH graph, and see multiple places where the pre activation bounds could be located
         3. Refer the ReLu example in the class and the diagonals to compute the slopes/intercepts
         4. The paper talks about 3 segments S+, S- and S+- for sigmoid and tanh. You should figure your own segments based on preactivation bounds for hardtanh.
         [1] https://arxiv.org/pdf/1811.00866.pdf
        """

        # You should return the linear lower and upper bounds after propagating through this layer.
        # Upper bound: uA is the coefficients, ubias is the bias.
        # Lower bound: lA is the coefficients, lbias is the bias.

        return uA, ubias, lA, lbias

