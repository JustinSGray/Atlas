from Atlas import Flags, JointProperties, PrescribedLoad, FBlade, \
                  MassProperties, FEM, Strains, Failure, Structures

import numpy as np
from scipy.io import loadmat

import unittest


class TestStructures(unittest.TestCase):

    def setUp(self):
        # input values from StrCalc.txt
        self.yN    = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.R     = 10
        self.b     = 2
        self.cE    = [0.2729, 1.3903, 1.1757, 1.0176, 0.8818, 0.7602, 0.6507, 0.5528, 0.4666, 0.3925]
        self.xEA   = [0.2700, 0.2711, 0.3039, 0.3272, 0.3138, 0.3004, 0.2870, 0.2736, 0.2601, 0.2467]
        self.xtU   = [0.0500, 0.1500, 0.1500, 0.1500, 0.1500, 0.1500, 0.1500, 0.1500, 0.1500, 0.1500]
        self.d     = [0.0843, 0.0780, 0.0718, 0.0655, 0.0592, 0.0530, 0.0477, 0.0431, 0.0384, 0.0338]
        self.theta = [0.3491, 0.3491, 0.3491, 0.3491, 0.3491, 0.3491, 0.3491, 0.3491, 0.3491, 0.3491]
        self.nTube = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.nCap  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.Jprop = JointProperties()
        self.Jprop.d = 0.0505
        self.Jprop.theta = 0.3491
        self.Jprop.nTube = 4
        self.Jprop.nCap = 0
        self.Jprop.lBiscuit = 0.3048

        self.yWire = [5.8852]
        self.zWire = 1
        self.tWire = 0.0016
        self.TWire = [1100]

        self.TEtension = 50
        self.ycmax = 1.4656

        self.lBiscuit = [0.3048, 0.3048, 0.3048, 0.3048, 0.3048, 0.3048, 0.2820, 0.2450, 0.2080, 0.1709]

        self.dQuad =  0.1016
        self.thetaQuad = 0.6109
        self.nTubeQuad = 4
        self.lBiscuitQuad = 0.3048
        self.RQuad = 14.1921
        self.hQuad = 3

        self.mElseRotor = 5.1100
        self.mElseCentre = 9.4870
        self.mElseR = 0.0320
        self.mPilot = 71

        self.Fblade = FBlade()
        self.Fblade.Fx = [-0.284403447526775, -0.870483325659561,  0.116391247565983,  0.498445425377258,  0.787764758081097,  0.946113366439064,  0.973141029534006,  1.136893103297792,  1.561570902385065,  1.085211015157862]
        self.Fblade.Fz = [ 0.154120235168162,  1.794087089172652,  6.804720170274912, 11.255449516620823, 15.786695216165727, 19.894719475495540, 23.261815364482230, 25.722247405087547, 27.261306866654838, 18.641003534034702]
        self.Fblade.My = [-0.008824032497880, -0.276404657165642, -0.728769459804588, -0.966127545968509, -1.199674646936011, -1.331716784492857, -1.362171707010043, -1.308986668710501, -1.199383590362132, -1.059498915491202]
        self.Fblade.Q  = [-0.142201723763388, -1.305724988489342,  0.290978118914957,  1.744558988820403,  3.544941411364938,  5.203623515414852,  6.325416691971040,  8.526698274733437, 13.273352670273054, 10.309504643999691]
        self.Fblade.P  = [-0.147424163931945, -1.353678490377422,  0.301664457843740,  1.808628922000631,  3.675131425465607,  5.394729584664550,  6.557721261428856,  8.839846177562180, 13.760824188353977, 10.688127137073966]
        self.Fblade.Pi = [-0.149830611246974, -1.397693658308050,  0.029633736804348,  1.191684379316726,  2.562641285650566,  3.674047046267912,  4.398254370459623,  6.004310658943595, 10.227652934084118,  6.460620820050246]
        self.Fblade.Pp = [ 0.002406447315028,  0.044015167930627,  0.272030721039391,  0.616944542683905,  1.112490139815042,  1.720682538396639,  2.159466890969234,  2.835535518618584,  3.533171254269860,  4.227506317023720]

        self.presLoad = PrescribedLoad()
        self.presLoad.y = 9.9999
        self.presLoad.pointZ = 1.4700
        self.presLoad.pointM = 0
        self.presLoad.distributedX = 0
        self.presLoad.distributedZ = 0
        self.presLoad.distributedM = 0

        self.flags = Flags()
        self.flags.Opt = 1
        self.flags.ConFail = 0
        self.flags.ConWireCont = 0
        self.flags.ConJigCont = 0
        self.flags.ConDef = 0
        self.flags.MultiPoint = 4
        self.flags.Quad = 1
        self.flags.FreeWake = 1
        self.flags.PlotWake = 0
        self.flags.DynamicClimb = 0
        self.flags.Cover = 0
        self.flags.Load =  0
        self.flags.Cdfit = 1
        self.flags.GWing = 1
        self.flags.AeroStr = 1
        self.flags.Movie = 0
        self.flags.wingWarp = 0
        self.flags.CFRPType = 'NCT301-1X HS40 G150 33 +/-2%RW'
        self.flags.WireType = 'Pianowire'

        # output values from StrCalc.txt
        self.Mtot   = 126.1670
        self.mSpar  = [0.2651, 0.2437, 0.2226, 0.2018, 0.1813, 0.1610, 0.1449, 0.1313, 0.1177, 0.1042]
        self.mChord = [0.0185, 0.1672, 0.1336, 0.1109, 0.0928, 0.0776, 0.0647, 0.0538, 0.0447, 0.0373]
        self.mQuad  = 4.7244
        self.mCover = 0
        self.mWire  = 0.0942
        self.EIx    = 1.0e+04 * np.array([2.2620, 1.7970, 1.4005, 1.0671, 0.7913, 0.5677, 0.4161, 0.3074, 0.2194, 0.1501])
        self.EIz    = 1.0e+04 * np.array([2.2620, 1.7970, 1.4005, 1.0671, 0.7913, 0.5677, 0.4161, 0.3074, 0.2194, 0.1501])
        self.EA     = 1.0e+07 * np.array([2.5129, 2.3273, 2.1418, 1.9562, 1.7706, 1.5850, 1.4292, 1.2919, 1.1546, 1.0173])
        self.GJ     = 1.0e+03 * np.array([6.6148, 5.2576, 4.1001, 3.1263, 2.3204, 1.6664, 1.2229, 0.9044, 0.6466, 0.4431])
        self.q = [
             0,       0,       0,       0,       0,       0,       0.0010, -0.0000, -0.0039, -0.0074, -0.0008,
            -0.0020,  0.0041, -0.0001, -0.0148, -0.0137, -0.0018, -0.0041,  0.0094, -0.0001, -0.0308, -0.0178,
            -0.0031, -0.0064,  0.0169, -0.0002, -0.0490, -0.0177, -0.0046, -0.0087,  0.0268, -0.0003, -0.0631,
            -0.0091, -0.0066, -0.0110,  0.0389, -0.0003, -0.0606,  0.0166, -0.0091, -0.0131,  0.0531, -0.0003,
            -0.0268,  0.0479, -0.0120, -0.0150,  0.0688, -0.0003,  0.0330,  0.0688, -0.0149, -0.0163,  0.0854,
            -0.0003,  0.1079,  0.0786, -0.0173, -0.0169,  0.1024, -0.0003,  0.1880,  0.0805, -0.0186, -0.0170
        ]
        self.EIQuad = 2.3706e+04
        self.GJQuad = 2.2828e+04
        self.Finternal = 1.0e+03 * np.array([
            0.0060,  0.0061,  0.0067,  0.0070,  0.0067,  0.0061,  0.0052,  0.0043,  0.0032,  0.0019, 0,
           -1.0845, -1.0845, -1.0845, -1.0845, -1.0845, -1.0845, -0.9600,  0.0000,  0.0000,  0.0000, 0,
           -0.0590, -0.0576, -0.0552, -0.0557, -0.0615, -0.0721, -0.0807,  0.0774,  0.0549,  0.0301, 0,
           -0.1975, -0.1396, -0.0845, -0.0292,  0.0319,  0.1036,  0.1861,  0.0918,  0.0367,  0.0065, 0,
           -0.0054, -0.0054, -0.0053, -0.0051, -0.0048, -0.0046, -0.0042, -0.0035, -0.0026, -0.0016, 0,
           -0.0478, -0.0417, -0.0351, -0.0280, -0.0212, -0.0151, -0.0098, -0.0055, -0.0023, -0.0004, 0,
        ])
        self.strain = {
            'top': [
                 0.000324431301337246,  0.000256654350930759,  0.000166969814378305,  3.54021221758653e-05, -0.000179059361519192,
                -0.000552190113896671, -0.000969951218287876, -0.000641588440001147, -0.000320224722824943, -8.09105043740408e-05, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                -3.43479597844849e-05, -3.93420100308486e-05, -4.42672276013990e-05, -5.07469212499079e-05, -5.90275454754569e-05,
                -6.64009851362718e-05, -6.81788516942396e-05, -6.22804500608437e-05, -4.76541279499912e-05, -2.04678186390271e-05, 0
            ],
            'bottom': [
                -0.000410742253294523, -0.000349847347261267, -0.000268237431845234, -0.000146276333313888, 5.65649060188704e-05,
                 0.000431063240542617,  0.000969951218287876,  0.000641588440001147,  0.000320224722824943, 8.09105043740409e-05,  0,
                 0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                -3.43479597844849e-05, -3.93420100308486e-05, -4.42672276013990e-05, -5.07469212499079e-05, -5.90275454754569e-05,
                -6.64009851362718e-05, -6.81788516942396e-05, -6.22804500608437e-05, -4.76541279499912e-05, -2.04678186390271e-05, 0
            ],
            'back': [
                -0.000132208563077293, -0.000137239632124606, -0.000140297772709814, -0.000141114679589468, -0.000140416760083675,
                -0.000130743918204572, -5.62383510852933e-05, -3.87302845541829e-05, -1.99497630809408e-05, -5.08949697520898e-06, 0,
                 0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                -3.43479597844849e-05, -3.93420100308486e-05, -4.42672276013990e-05, -5.07469212499079e-05, -5.90275454754569e-05,
                -6.64009851362718e-05, -6.81788516942396e-05, -6.22804500608437e-05, -4.76541279499912e-05, -2.04678186390271e-05, 0
            ],
            'front': [
                 4.58976111200157e-05,  4.40466357940974e-05,  3.90301552428856e-05,  3.02404684514454e-05,  1.79223045833536e-05,
                 9.61704485051833e-06,  5.62383510852934e-05,  3.87302845541831e-05,  1.99497630809410e-05,  5.08949697520909e-06, 0,
                 0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                -3.43479597844849e-05, -3.93420100308486e-05, -4.42672276013990e-05, -5.07469212499079e-05, -5.90275454754569e-05,
                -6.64009851362718e-05, -6.81788516942396e-05, -6.22804500608437e-05, -4.76541279499912e-05, -2.04678186390271e-05, 0
            ],
            'bending_x': [
                -8.90530870986543e-05, -9.06431339593515e-05, -8.96639639763497e-05, -8.56775740204565e-05, -7.91695323335143e-05,
                -7.01804815275453e-05, -5.62383510852933e-05, -3.87302845541830e-05, -1.99497630809409e-05, -5.08949697520904e-06, 0
            ],
            'bending_z': [
                 0.000367586777315884,  0.000303250849096013,  0.000217603623111769,  9.08392277448765e-05, -0.000117812133769031,
                -0.000491626677219644, -0.000969951218287876, -0.000641588440001147, -0.000320224722824943, -8.09105043740408e-05, 0
            ],
            'axial_y': [
                -4.31554759786386e-05, -4.65964981652541e-05, -5.06338087334642e-05, -5.54371055690111e-05, -6.12472277501607e-05,
                -6.05634366770269e-05,  5.42101086242752e-20,  1.08420217248550e-19,  1.08420217248550e-19,  5.42101086242752e-20, 0
            ],
            'torsion_y': [
                -3.43479597844849e-05, -3.93420100308486e-05, -4.42672276013990e-05, -5.07469212499079e-05, -5.90275454754569e-05,
                -6.64009851362718e-05, -6.81788516942396e-05, -6.22804500608437e-05, -4.76541279499912e-05, -2.04678186390271e-05, 0
            ]
        }
        self.fail = {
            'top': {
                'cap': np.zeros((3, 11)),

                'plus': [
                     0.0284056598067858,   0.0220735476027992,   0.0137497301758022,   0.00156302383714983, -0.0441046203021050,
                    -0.126863798140737,   -0.219009394673833,   -0.146226312533080,   -0.0742941768089941,  -0.0194384389147555,  0,
                     0.0318448674839274,   0.0259292216986276,   0.0179995220398921,   0.00632145100424583, -0.00215607064524889,
                    -0.00782379900472648, -0.0142352598316179,  -0.00924154332506846, -0.00444422263751008, -0.00103729098314935, 0,
                    -0.00655602066494422, -0.00544664484656088, -0.00394269333196902, -0.00172044360420772,  0.00195071768154226,
                     0.00848839668802907,  0.0159465690832996,   0.0101806514274382,   0.00472696523760348,  0.00101414190814641, 0
                ],
                'minus': [
                     0.0306516581316693,   0.0246461047264613,   0.0166443451591611,   0.00488134320270856,  -0.0347650820386925,
                    -0.116357609268859,   -0.208221905730749,   -0.136372088683510,   -0.0667541792059505,   -0.0161999512932897, 0,
                     0.0276842464869834,   0.0211636637434136,   0.0126373649338952,   0.000174398678360763, -0.00335553155314803,
                    -0.00917309085271744, -0.0156206785661085,  -0.0105071044215468,  -0.00541257161959346,  -0.00145320440339635, 0,
                     0.00508699270088119,  0.00376402633703683,  0.00204942818184007, -0.000449951577164631, -0.00447526689778466,
                    -0.0113283005605897,  -0.0188625105344069,  -0.0128443241267155,  -0.00676508473584494,  -0.00188953008644754, 0
                ]
            },
            'bottom': {
                'cap': np.zeros((3, 11)),

                'plus': [
                    -0.0931764863820579,  -0.0801604822384388,  -0.0625768957725388,  -0.0362296084758924,    0.00321845686982193,
                     0.0370629778031000,   0.0860526438589149,   0.0563590018955698,   0.0275877487008108,    0.00669501431312352, 0,
                    -0.00597251967806871, -0.00498458026256345, -0.00367852723623861, -0.00173565827546095,   0.00876452733835199,
                     0.0435690016943585,   0.0931163046862603,   0.0626338178937925,   0.0322648382996480,    0.00866268539009956, 0,
                     0.00663573285498099,  0.00543625601617850,  0.00386654665782075,  0.00153954499250117,  -0.00227725983627241,
                    -0.00915483301968193, -0.0188625105344069,  -0.0128443241267156,  -0.00676508473584493,  -0.00188953008644754, 0
                ],

                'minus': [
                    -0.0877418357948886,  -0.0739356560986589,  -0.0555727850193590,  -0.0282002586368252,   0.00707824269383313,
                     0.0414049096768541,   0.0905108296626293,   0.0604314937520682,   0.0307038316420111,   0.00803339617526951,  0,
                    -0.00667048254770408, -0.00578402402547241, -0.00457805318774593, -0.00276685392734197,  0.00161443031238016,
                     0.0355257486246225,   0.0848576959162941,   0.0550896915512634,   0.0264924207649873,   0.00618338715738059,  0,
                    -0.00810476081904397, -0.00711887452570261, -0.00575981180794971, -0.00370994017387353, -0.000247289379969967,
                     0.00631492914712137,  0.0159465690832996,   0.0101806514274383,   0.00472696523760350,  0.00101414190814641,  0
                ]
            },
            'back': {
                'cap': np.zeros((3, 11)),

                'plus': [
                    -0.0318340660446484,   -0.0333371632398721,   -0.0344003102313462,   -0.0350928399501440,   -0.0355942289798210,
                    -0.0340472714735883,   -0.0177793074842833,   -0.0134568139980143,   -0.00816360286280569,  -0.00274012101059969,  0,
                    -0.00168576559187046,  -0.00171245547612000,  -0.00170948048947762,  -0.00165621818985608,  -0.00156134427848213,
                    -0.00133755958396985,  -0.000172823204875201,  0.000218800101627640,  0.00105594190460327,   0.000772719377701380, 0,
                     0.00163780037333550,   0.00162128122982061,   0.00157083234913204,   0.00144692568749659,   0.00125732539302155,
                     0.000926081231422341, -0.000448845109962313, -0.000636870699179088, -0.000661086647821561, -0.000346369545150895, 0
                ],
                'minus': [
                    -0.0263994154574792,  -0.0271123371000923,  -0.0273961994781665,  -0.0270634901110767,   -0.0262546907164085,
                    -0.0235410826017107,  -0.00699181854119932, -0.00360259014844468, -0.000623605259762018,  0.000205961828682410, 0,
                    -0.00238372846150582, -0.00251189923902896, -0.00260900644098494, -0.00268741384173711,  -0.00276080518638126,
                    -0.00268685143196081, -0.00155824193936580, -0.00122885639616545, -0.000791209982293074, -0.000286286272117077, 0,
                    -0.00310682833739850, -0.00330389973934471, -0.00346409749926100, -0.00361732086886895,  -0.00378187460926391,
                    -0.00376598510398294, -0.00246709634114486, -0.00202680200009824, -0.00137703285041992,  -0.000529018633150231, 0
                ]
            },
            'front': {
                'cap': np.zeros((3, 11)),

                'plus': [
                     0.00305444888489182,  0.00272269986209007,  0.00210508754213125,  0.00109322726722145,  -0.000722679139433743,
                    -0.00313509999453344,  0.00288953493505142,  0.00148885587193993,  0.000257719672377998, -0.000498366610866154, 0,
                     0.00629113126714338,  0.00642378425578826,  0.00626185289594772,  0.00584790133198415,   0.00521930865028814,
                     0.00490393067230818,  0.00928882382329451,  0.00732532624090147,  0.00471647563005752,   0.00170657885501761,  0,
                    -0.00155808818329869, -0.00163167006020299, -0.00164697902328030, -0.00162782429920312,  -0.00158386754775168,
                    -0.00159251756307525, -0.00246709634114486, -0.00202680200009825, -0.00137703285041992,  -0.000529018633150233, 0
                ],
                'minus': [
                     0.00530044720977534,   0.00529525698575218,   0.00499970252549016,   0.00441154663278018,   0.00356112151973586,
                     0.00304627740193059,   0.00734772073876582,   0.00556134772843825,   0.00337380261357822,   0.00113242003346359,  0,
                     0.00213051027019948,   0.00165822630057415,   0.000899695789950728, -5.01839235803326e-05, -0.000323898426783084,
                    -0.000526635439956877,  0.00103021505332878,  -3.67047003129318e-05, -0.000177138999790288, -0.000129627148129919, 0,
                     8.90602192356987e-05, -5.09484493211032e-05, -0.000246286126848654, -0.000542570882169224, -0.000940681668490701,
                    -0.00124738630948535,  -0.000448845109962305, -0.000636870699179088, -0.000661086647821556, -0.000346369545150893, 0
                ]
            },
            'buckling': {
                'x': [0.394669203912155, 0.394669203912155, 0.394669203912155, 0.394669203912155, 0.394669203912155, 0.394669203912155, 0, 0, 0, 0, 0],
                'z': [0.394669203912155, 0.394669203912155, 0.394669203912155, 0.394669203912155, 0.394669203912155, 0.394669203912155, 0, 0, 0, 0, 0],
                'torsion': [
                    0.0249803622153795, 0.0274166207230945, 0.0298385589887717, 0.0318005580862193, 0.0344072425546554,
                    0.0376229852836405, 0.0371306344531331, 0.0327850625738252, 0.0259578917805189, 0.0168665337743183,  0
                ]
            },
            'quad': {
                'buckling': 1.0354,
                'bend': 0.9098,
                'torsion': 0.1489,
                'torbuck': 3.4352
            },
            'wire': 0.2088
        }

        # output values from ChordProperties.txt
        self.xCGChord = [0.3748, 0.2925, 0.2945, 0.2963, 0.2984, 0.3007, 0.3035, 0.3068, 0.3106, 0.3150]
        self.xEA      = [0.2700, 0.2711, 0.3039, 0.3272, 0.3138, 0.3004, 0.2870, 0.2736, 0.2601, 0.2467]

        # output values from WireProperties.txt (wire type == 1, Pianowire)
        self.RHO   = 7850

    def tearDown(self):
        pass

    def test_MassProperties(self):
        comp = MassProperties()

        # populate inputs
        comp.flags = self.flags

        comp.b        = self.b

        comp.mSpar    = self.mSpar
        comp.mChord   = self.mChord
        comp.xCGChord = self.xCGChord
        comp.xEA      = self.xEA
        comp.mQuad    = self.mQuad

        comp.ycmax    = self.ycmax

        comp.yWire    = self.yWire
        comp.zWire    = self.zWire
        comp.tWire    = self.tWire
        comp.RHOWire  = self.RHO

        comp.mElseRotor  = self.mElseRotor
        comp.mElseCentre = self.mElseCentre
        comp.mElseR      = self.mElseR
        comp.R           = self.R
        comp.mPilot      = self.mPilot

        # run
        comp.run()

        # check outputs
        self.assertAlmostEquals(comp.Mtot, self.Mtot, delta=0.0011)

    def test_FEM(self):
        comp = FEM()

        data = loadmat('FEM.mat', struct_as_record=True, mat_dtype=True)

        # populate inputs
        comp.flags = Flags()
        comp.flags.Load = int(data['flags']['Load'][0][0][0][0])
        comp.flags.wingWarp = int(data['flags']['wingWarp'][0][0][0][0])

        comp.yN  = data['yN']

        comp.EIx = data['EIx']
        comp.EIz = data['EIz']
        comp.EA  = data['EA']
        comp.GJ  = data['GJ']

        comp.cE  = data['cE']
        comp.xEA = data['xEA']

        comp.Fblade = FBlade()
        comp.Fblade.Fx = data['Fblade']['Fx'][0][0].flatten()
        comp.Fblade.Fz = data['Fblade']['Fz'][0][0].flatten()
        comp.Fblade.My = data['Fblade']['My'][0][0].flatten()
        comp.Fblade.Q  = data['Fblade']['Q'][0][0].flatten()
        comp.Fblade.P  = data['Fblade']['P'][0][0].flatten()
        comp.Fblade.Pi = data['Fblade']['Pi'][0][0].flatten()
        comp.Fblade.Pp = data['Fblade']['Pp'][0][0].flatten()

        comp.mSpar  = data['mSpar']
        comp.mChord = data['mChord']
        comp.xCG    = data['xCG']

        comp.yWire = data['yWire'].flatten()
        comp.zWire = data['zWire'][0][0]
        comp.TWire = data['TWire'].flatten()

        comp.presLoad = PrescribedLoad()
        comp.presLoad.y = data['presLoad']['y'][0][0][0][0]
        comp.presLoad.pointZ = data['presLoad']['pointZ'][0][0][0][0]
        comp.presLoad.pointM = data['presLoad']['pointM'][0][0][0][0]
        comp.presLoad.distributedX = data['presLoad']['distributedX'][0][0][0][0]
        comp.presLoad.distributedZ = data['presLoad']['distributedZ'][0][0][0][0]
        comp.presLoad.distributedM = data['presLoad']['distributedM'][0][0][0][0]

        # run
        comp.run()

        # check outputs
        for h, plane in enumerate(data['k']):
            for i, row in enumerate(plane):
                for j, val in enumerate(row):
                    self.assertAlmostEquals(comp.k[h, i, j], val, 4,
                        msg='k[%d, %d, %d] mismatch (%f vs %f)' % (h, i, j, comp.k[h, i, j], val))

        for i, row in enumerate(data['K']):
            for j, val in enumerate(row):
                self.assertAlmostEquals(comp.K[i, j], val, 4,
                    msg='K[%d, %d] mismatch (%f vs %f)' % (i, j, comp.K[i, j], val))

        for i, val in enumerate(data['F']):
            self.assertAlmostEquals(comp.F[i], val, 4,
                msg='F[%d] mismatch (%f vs %f)' % (i, comp.F[i], val))

        for i, val in enumerate(data['q']):
            self.assertAlmostEquals(comp.q[i], val, 4,
                msg='q[%d] mismatch (%f vs %f)' % (i, comp.q[i], val))

    def test_Strains(self):
        comp = Strains()

        # populate inputs from MATLAB test data
        data = loadmat('strains.mat', struct_as_record=True)
        comp.yN = data['yN']
        comp.d  = data['d']
        comp.k  = data['k']
        comp.F  = data['F']
        comp.q  = data['q']

        # run
        comp.run()

        # check outputs
        for i, row in enumerate(data['Finternal']):
            for j, val in enumerate(row):
                self.assertAlmostEquals(comp.Finternal[i, j], val, 4,
                    msg='Finternal[%d, %d] mismatch (%f vs %f)' % (i, j, comp.Finternal[i, j], val))

        for i, row in enumerate(data['strain']['top'][0]):
            for j, val in enumerate(row[0]):
                self.assertAlmostEquals(comp.strain.top[i, j], val, 4,
                    msg='strain.top[%d, %d] mismatch (%f vs %f)' % (i, j, comp.strain.top[i, j], val))

        for i, row in enumerate(data['strain']['bottom'][0]):
            for j, val in enumerate(row[0]):
                self.assertAlmostEquals(comp.strain.bottom[i, j], val, 4,
                    msg='strain.bottom[%d, %d] mismatch (%f vs %f)' % (i, j, comp.strain.bottom[i, j], val))

        for i, row in enumerate(data['strain']['back'][0]):
            for j, val in enumerate(row[0]):
                self.assertAlmostEquals(comp.strain.back[i, j], val, 4,
                    msg='strain.back[%d, %d] mismatch (%f vs %f)' % (i, j, comp.strain.back[i, j], val))

        for i, row in enumerate(data['strain']['front'][0]):
            for j, val in enumerate(row[0]):
                self.assertAlmostEquals(comp.strain.front[i, j], val, 4,
                    msg='strain.bottom[%d, %d] mismatch (%f vs %f)' % (i, j, comp.strain.front[i, j], val))

        for i, row in enumerate(data['strain']['bending_x']):
            for j, val in enumerate(row[0][0]):
                self.assertAlmostEquals(comp.strain.bending_x[i][j], val, 4,
                    msg='strain.bending_x[%d, %d] mismatch (%f vs %f)' % (i, j, comp.strain.bending_x[i, j], val))

        for i, row in enumerate(data['strain']['bending_z']):
            for j, val in enumerate(row[0][0]):
                self.assertAlmostEquals(comp.strain.bending_z[i][j], val, 4,
                    msg='strain.bending_z[%d, %d] mismatch (%f vs %f)' % (i, j, comp.strain.bending_z[i, j], val))

        for i, row in enumerate(data['strain']['axial_y']):
            for j, val in enumerate(row[0][0]):
                self.assertAlmostEquals(comp.strain.axial_y[i][j], val, 4,
                    msg='strain.axial_y[%d, %d] mismatch (%f vs %f)' % (i, j, comp.strain.axial_y[i, j], val))

        for i, row in enumerate(data['strain']['torsion_y']):
            for j, val in enumerate(row[0][0]):
                self.assertAlmostEquals(comp.strain.torsion_y[i][j], val, 4,
                    msg='strain.torsion_y[%d, %d] mismatch (%f vs %f)' % (i, j, comp.strain.torsion_y[i, j], val))

    def test_Failure(self):
        comp = Failure()
        # populate inputs
        comp.yN  = self.yN
        comp.d   = self.d

    def test_Structures(self):
        comp = Structures()

        # populate inputs
        comp.yN    = self.yN
        comp.R     = self.R
        comp.b     = self.b
        comp.cE    = self.cE
        comp.xEA   = self.xEA
        comp.xtU   = self.xtU
        comp.d     = self.d
        comp.theta = self.theta
        comp.nTube = self.nTube
        comp.nCap  = self.nCap

        comp.Jprop = self.Jprop

        comp.yWire = self.yWire
        comp.zWire = self.zWire
        comp.tWire = self.tWire
        comp.TWire = self.TWire

        comp.TEtension = self.TEtension
        comp.ycmax = self.ycmax

        comp.lBiscuit = self.lBiscuit

        comp.dQuad =  self.dQuad
        comp.thetaQuad = self.thetaQuad
        comp.nTubeQuad = self.nTubeQuad
        comp.lBiscuitQuad = self.lBiscuitQuad
        comp.RQuad = self.RQuad
        comp.hQuad = self.hQuad

        comp.mElseRotor = self.mElseRotor
        comp.mElseCentre = self.mElseCentre
        comp.mElseR = self.mElseR
        comp.mPilot = self.mPilot

        comp.Fblade = self.Fblade
        comp.presLoad = self.presLoad
        comp.flags = self.flags

        # run
        comp.run()

        # check outputs
        self.assertAlmostEquals(comp.Mtot, self.Mtot, 4)

        for i, val in enumerate(self.mSpar):
            self.assertAlmostEquals(comp.mSpar[i], self.mSpar[i], 4)
        for i, val in enumerate(self.mChord):
            self.assertAlmostEquals(comp.mChord[i], self.mChord[i], 4)

        self.assertAlmostEquals(comp.mQuad,  self.mQuad,  4)
        self.assertAlmostEquals(comp.mCover, self.mCover, 4)
        self.assertAlmostEquals(comp.mWire,  self.mWire,  4)

        for i, val in enumerate(self.EIx):
            self.assertAlmostEquals(comp.EIx[i], self.EIx[i], 4)
        for i, val in enumerate(self.EIz):
            self.assertAlmostEquals(comp.EIz[i], self.EIz[i], 4)
        for i, val in enumerate(self.EA):
            self.assertAlmostEquals(comp.EA[i], self.EA[i], 4)
        for i, val in enumerate(self.GJ):
            self.assertAlmostEquals(comp.GJ[i], self.GJ[i], 4)
        for i, val in enumerate(self.q):
            self.assertAlmostEquals(comp.q[i], self.q[i], 4)

        self.assertAlmostEquals(comp.EIQuad, self.EIQuad, 4)
        self.assertAlmostEquals(comp.GJQuad, self.GJQuad, 4)

        for i, val in enumerate(self.Finternal):
            self.assertAlmostEquals(comp.Finternal[i], self.Finternal[i], 4)


if __name__ == "__main__":
    unittest.main()
