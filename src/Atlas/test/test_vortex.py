from Atlas import vortexWake
import numpy as np
import unittest

def relative_err(x, y):
    return (np.abs(x-y)/np.linalg.norm(x)).max()

class AtlasTestVortex(unittest.TestCase):

    def test_vortexWakeCover(self):
        comp = vortexWake()
        comp.yN = np.array([0,1,2,3,4,5,6,7,8,9,10])
        comp.rho = 1.18
        comp.dT = np.array([0.0649,  1.5887,  6.8049, 11.2556, 15.7854, 19.8941, 23.2617, 25.7216, 27.2537, 18.6446])
        comp.vc = 0
        comp.Omega = 1.0367
        comp.b = 2
        comp.h = 1.5
        comp.Nw = 8
        comp.Ntt = 3
        comp.Ntheta = 20
        comp.qh = np.array([0, -0.0179, -0.0427, -0.0727, -0.1049, -0.1331, -0.1445, -0.1247, -0.0789, -0.0181,  0.0480])
        comp.ycmax = 1.4656
        comp.flag_cover = 0
        comp.flag_plot = 0
        comp.flag_dynamic_climb = 0

        comp.run()


        comp.vi = np.array([-1.0343, -0.7853,  0.0044,  0.1058,  0.1622,  0.1846,  0.1890,  0.2333,  0.3749,  0.3463])
        comp.ring_gamma = np.array([[-0.1061, -0.7597, -1.3592, -0.4038, -0.2387, -0.0893, 0.0314, 0.1219, 0.1825, 1.0167, 1.6043],
                        [-0.1061, -0.7597, -1.3592, -0.4038, -0.2387, -0.0893, 0.0314, 0.1219, 0.1825, 1.0167, 1.6043],
                        [-0.1061, -0.7597, -1.3592, -0.4038, -0.2387, -0.0893, 0.0314, 0.1219, 0.1825, 1.0167, 1.6043],
                        [-0.1061, -0.7597, -1.3592, -0.4038, -0.2387, -0.0893, 0.0314, 0.1219, 0.1825, 1.0167, 1.6043],
                        [-0.1061, -0.7597, -1.3592, -0.4038, -0.2387, -0.0893, 0.0314, 0.1219, 0.1825, 1.0167, 1.6043],
                        [-0.1061, -0.7597, -1.3592, -0.4038, -0.2387, -0.0893, 0.0314, 0.1219, 0.1825, 1.0167, 1.6043],
                        [-0.1061, -0.7597, -1.3592, -0.4038, -0.2387, -0.0893, 0.0314, 0.1219, 0.1825, 1.0167, 1.6043],
                        [-0.1061, -0.7597, -1.3592, -0.4038, -0.2387, -0.0893, 0.0314, 0.1219, 0.1825, 1.0167, 1.6043],
                        [-0.1061, -0.7597, -1.3592, -0.4038, -0.2387, -0.0893, 0.0314, 0.1219, 0.1825, 1.0167, 1.6043]])
        comp.ring_z = np.array([[0,-0.0179,-0.0427,-0.0727,-0.1049,-0.1331,-0.1445,-0.1247,-0.0789,-0.0181,0.0480],
                        [4.3650,3.4844,1.4734, -0.1832, -0.4967, -0.6037, -0.6548, -0.7272, -0.9647, -1.1323, -0.5478],
                        [8.3534,7.7421,3.9743,0.3141, -0.6242, -0.9542, -1.0269, -1.1753, -1.2898, -1.2922, -0.7336],
                        [12.3919, 11.3197,6.8925,1.5800, -0.1373, -1.1272, -1.2458, -1.4511, -1.2743, -1.3069, -0.7107],
                        [14.2779, 13.6723, 10.2982,5.1922,2.7432, -1.1962, -1.3874, -1.4342, -1.3367, -1.4767, -1.3679],
                        [14.2806, 11.7627, 12.8245, 11.9737,6.3292, -1.1116, -1.4835, -1.4425, -1.2710, -1.0455, -0.8828],
                        [14.2806,8.6037, 10.0749,7.7824, 11.8290, -0.5869, -1.4866, -1.4150, -0.7794, -0.1461, -0.2328],
                        [14.2806,6.0348,7.5962, 11.3184, 13.9287,1.4405, -1.4825, -1.2298, -0.1680, -0.2191, -0.9765],
                        [14.2806,3.7014,4.0474, 10.0053, 12.5491,5.6841, -1.4890, -1.2901, -0.3161, -0.0462, -0.9405]])
        comp.ring_r = np.array([[0, 1.0000, 2.0000, 3.0000, 4.0000, 5.0000, 6.0000, 7.0000, 8.0000, 9.0000, 10.0000],
                        [-0.0000, 0.7154, 1.4624, 2.5962, 3.8166, 4.9714, 6.0923, 7.3218, 8.6759, 10.1604, 10.5758],
                        [-0.0000, 0.8163, 1.2187, 1.8561, 3.0175, 4.6630, 6.3119, 8.2025, 11.1961, 13.4735, 12.2798],
                        [0.0000, 0.6150, 1.4916, 2.0744, 1.5386, 4.0188, 6.7222, 10.4076, 14.1699, 15.9107, 14.3565],
                        [0.0000, 1.4536, 1.3686, 1.6554, 0.7565, 2.9299, 7.5369, 13.9772, 16.6633, 20.3688, 19.7788],
                        [0.0000, 2.8403, 1.5305, 0.9715, 0.7507, 1.6326, 9.5092, 16.7389, 20.7242, 21.7340, 21.2857],
                        [0.0000, 2.9776, 2.9841, 1.9832, 0.5341, 0.7735, 13.9370, 20.8148, 21.6299, 20.5856, 18.8682],
                        [0.0000, 2.2892, 2.6480, 2.5465, 0.5236, 0.2493, 16.8681, 21.8780, 17.7853, 16.4244, 16.8469],
                        [0.0000, 2.8366, 2.0276, 2.1377, 2.4799, 0.3460, 20.6910, 21.9446, 16.5073, 12.7431, 19.6353]])
        comp.ring_vz = np.array([[1.5544, 1.1726, 0.5631, 0.0530, -0.0823, -0.1127, -0.1139, -0.1279, -0.1875, -0.2816, -0.1509],
                        [1.2870, 1.4665, 0.9392, 0.2454, -0.0131, -0.0711, -0.0763, -0.0990, -0.0179, 0.0007, -0.1349],
                        [1.3218, 1.4424, 0.8700, 0.1597, 0.2975, -0.0312, -0.0424, -0.0520, -0.0164, -0.0393, 0.0092],
                        [0.6808, 0.5685, 1.0282, 0.7760, 0.9163, 0.0036, -0.0273, -0.0017, -0.0349, 0.0011, -0.0128],
                        [0.6760, 0.1538, 0.7476, 1.0109, 1.1409, 0.0766, -0.0175, -0.0113, 0.0089, 0.0768, 0.0644],
                        [0.6759, 0.1464, 0.1609, 0.7696, 1.4000, 0.2775, -0.0002, 0.0031, 0.1142, 0.0864, -0.0884],
                        [0.6759, 0.1935, 0.2533, 0.3514, 1.0784, 0.8912, -0.0025, 0.0497, -0.1109, -0.0671, -0.0329],
                        [0.6759, -0.0599, 0.4602, 0.5641, 0.1934, 1.2289, 0.0004, 0.0397, -0.0565, -0.0250, -0.0336],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.]])
        comp.ring_vr = np.array([[-0.0000, -0.1016, -0.1261, -0.1583, -0.0922, -0.0266, 0.0171, 0.1016, 0.2599, 0.5590, 0.2654],
                        [-0.0000, 0.0632, -0.1198, -0.1801, -0.2356, -0.1160, 0.0601, 0.2792, 0.9469, 0.9825, 0.5139],
                        [0.0000, 0.0453, -0.0634, 0.0978, -0.3585, -0.2193, 0.1200, 0.8825, 0.9015, 0.7864, 0.5410],
                        [0.0000, 0.2625, -0.0428, 0.1173, -0.1879, -0.3728, 0.2259, 0.9549, 0.8686, 0.8719, 0.9135],
                        [0.0000, 0.2027, 0.0977, 0.0218, -0.1041, -0.3898, 0.5972, 0.8978, 0.7915, 0.5428, 0.5682],
                        [0.0000, 0.0106, 0.0756, -0.0079, 0.1118, -0.2114, 0.9625, 0.8054, 0.4646, 0.2257, 0.2349],
                        [0.0000, -0.1301, -0.0364, 0.0530, 0.0706, -0.0584, 0.9066, 0.5447, 0.2338, 0.2136, 0.7111],
                        [0.0000, -0.0157, -0.0224, -0.0109, 0.3042, -0.0027, 0.8255, 0.5302, 0.2756, 0.1160, 0.7243],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])




if __name__ == "__main__":
    unittest.main()