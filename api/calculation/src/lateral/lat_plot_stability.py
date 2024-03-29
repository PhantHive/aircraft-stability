import numpy as np
from matplotlib import pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class PlotLateralModes:

    def __init__(self, eigenvalues, eigenvectors):
        self.eigenvalues = eigenvalues
        self.eigenvectors = eigenvectors

    def plot_modes(self, mode):


        # calculate response for selected mode
        if mode == 'Rolling':

            t = np.linspace(0, 20, 1000)
            lambda_roll = self.eigenvalues[1]
            # initial conditions
            v0 = self.eigenvectors[0][1]
            p0 = self.eigenvectors[1][1]
            r0 = self.eigenvectors[2][1]
            phi0 = self.eigenvectors[3][1]
            # calculate side velocity
            v = v0 * np.exp(lambda_roll * t)
            # calculate roll rate
            p = p0 * np.exp(lambda_roll * t)
            # calculate yaw rate
            r = r0 * np.exp(lambda_roll * t)
            # calculate side angle
            phi = phi0 * np.exp(lambda_roll * t)

            print("\nRolling mode parameter:")
            print("Lambda_roll", lambda_roll)

        elif mode == 'Spiral':
            t = np.linspace(0, 2500, 1000)
            # plot spiral mode
            lambda_spiral = self.eigenvalues[3]
            # initial conditions
            v0 = self.eigenvectors[0][3]
            p0 = self.eigenvectors[1][3]
            r0 = self.eigenvectors[2][3]
            phi0 = self.eigenvectors[3][3]

            # calculate side velocity
            v = v0 * np.exp(lambda_spiral * t)
            # calculate roll rate
            p = p0 * np.exp(lambda_spiral * t)
            # calculate yaw rate
            r = r0 * np.exp(lambda_spiral * t)
            # calculate side angle
            phi = phi0 * np.exp(lambda_spiral * t)

            print("\nSpiral mode parameter:")
            print("Lambda_spiral", lambda_spiral)


        elif mode == 'Dutch Roll':

            t = np.linspace(0, 100, 1000)

            # plot dutch roll mode
            lambda_dutch = self.eigenvalues[2]

            wn_dutch_roll = np.sqrt(lambda_dutch.real ** 2 + lambda_dutch.imag ** 2)

            zeta_dutch_roll = - lambda_dutch.real / wn_dutch_roll

            print("\nDutch roll mode parameters:")
            print("(Natural frequency) wn_dutch_roll = ", wn_dutch_roll)
            print("(Damping factor) zeta_dutch_roll = ", zeta_dutch_roll)

            # initial conditions

            v0 = self.eigenvectors[0][2]  # good

            p0 = self.eigenvectors[1][2]  # good

            r0 = self.eigenvectors[2][2]  # good

            phi0 = self.eigenvectors[3][2]  # good

            # calculate side velocity
            v = np.exp(- wn_dutch_roll * zeta_dutch_roll * t) * (v0 * np.cos((wn_dutch_roll * np.sqrt(1 - zeta_dutch_roll ** 2)) * t) + ((v0 * wn_dutch_roll * zeta_dutch_roll)/(wn_dutch_roll * np.sqrt(1 - zeta_dutch_roll ** 2))) * np.sin((wn_dutch_roll * np.sqrt(1 - zeta_dutch_roll ** 2)) * t))

            # calculate roll rate
            p = np.exp(- wn_dutch_roll * zeta_dutch_roll * t) * (p0 * np.cos((wn_dutch_roll * np.sqrt(1 - zeta_dutch_roll ** 2)) * t) + ((p0 * wn_dutch_roll * zeta_dutch_roll)/(wn_dutch_roll * np.sqrt(1 - zeta_dutch_roll ** 2))) * np.sin((wn_dutch_roll * np.sqrt(1 - zeta_dutch_roll ** 2)) * t))

            # calculate yaw rate
            r = np.exp(- wn_dutch_roll * zeta_dutch_roll * t) * (r0 * np.cos((wn_dutch_roll * np.sqrt(1 - zeta_dutch_roll ** 2)) * t) + ((r0 * wn_dutch_roll * zeta_dutch_roll)/(wn_dutch_roll * np.sqrt(1 - zeta_dutch_roll ** 2))) * np.sin((wn_dutch_roll * np.sqrt(1 - zeta_dutch_roll ** 2)) * t))

            # calculate side angle
            phi = np.exp(- wn_dutch_roll * zeta_dutch_roll * t) * (phi0 * np.cos((wn_dutch_roll * np.sqrt(1 - zeta_dutch_roll ** 2)) * t) + ((phi0 * wn_dutch_roll * zeta_dutch_roll)/(wn_dutch_roll * np.sqrt(1 - zeta_dutch_roll ** 2))) * np.sin((wn_dutch_roll * np.sqrt(1 - zeta_dutch_roll ** 2)) * t))

        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)

        # plot all curves on the same graph
        plt.plot(t, v, 'blue', label='Side velocity')
        plt.plot(t, p, 'red', label='Roll rate')
        plt.plot(t, r, 'orange', label='Yaw rate')
        plt.plot(t, phi, 'purple', label='Side angle')
        # add legend
        plt.legend(loc='upper right')

        plt.xlabel('Time (s)')
        plt.title(f'{mode} Mode Response')

        # # Move left y-axis and bottom x-axis to left, passing through (0,0)
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        # # Eliminate upper and right axes
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        # # Show ticks in the left and lower axes only
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        plt.grid(True)
        # plt.show()

        # Render the plot as a bitmap or vector graphics format
        canvas = FigureCanvas(fig)
        buf = io.BytesIO()
        canvas.print_png(buf)  # Or use print_svg or print_pdf for other formats

        # Convert the rendered plot to a binary data payload
        data = base64.b64encode(buf.getvalue()).decode('utf-8')

        return data
