import os # Biblioteca que mexe com o Sistema Operacional do PC

class xfoil:

    def __init__(self, airfoil_name, alpha_i, alpha_f, alpha_step, Re, M, n_iter):
        self.airfoil_name = airfoil_name
        self.alpha_i = alpha_i
        self.alpha_f = alpha_f
        self.alpha_step = alpha_step
        self.Re = Re
        self.M = M
        self.n_iter = n_iter
        pass

    def input_xfoil(self):
        if os.path.exists("polar_file.txt"):
            os.remove("polar_file.txt")

        # Cada ação descrita a seguir corresponde a um comando interno no programa Xfoil

        input_file = open("input_file.in", 'w')
        input_file.write("\nPLOP\nG\n\n")
        input_file.write("LOAD {0}.dat\n".format(self.airfoil_name))
        input_file.write(self.airfoil_name + '\n')
        input_file.write("PANE\n")
        input_file.write("OPER\n")
        input_file.write("Visc {0}\n".format(self.Re))
        input_file.write("M\n {0}\n".format(self.M))
        input_file.write("PACC\n")
        input_file.write("polar_file.txt\n\n")
        input_file.write("ITER {0}\n".format(self.n_iter))
        input_file.write("ASeq {0} {1} {2}\n".format(self.alpha_i, self.alpha_f, self.alpha_step))
        input_file.write("\n\n")
        input_file.write("quit\n")
        input_file.close()
                
        return open("input_file.in", 'r')
