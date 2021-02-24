# -------------------------------------------------------
# Assignment 1
# Written by Michel Rahme 40038465
# For COMP 472 Section IX – Summer 2020
# --------------------------------------------------------

import shapefile as shp  # Requires the pyshp package
import matplotlib.pyplot as plt
import matplotlib as mpl
from threading import Timer
from math import floor
from a_star import *

mpl.use("TkAgg")


class CrimePlot:
    def __init__(self, threshold, grid_size):
        # Read data from shapefile
        shape = shp.Reader("Shape/crime_dt.shp", encoding='ISO-8859-1')
        shape_records = shape.shapeRecords()
        self.shape_points = np.empty([len(shape_records), 2])
        # Arrange data in list
        for i in range(len(shape_records)):
            x = shape_records[i].shape.__geo_interface__["coordinates"][0]
            y = shape_records[i].shape.__geo_interface__["coordinates"][1]
            self.shape_points[i] = [x, y]
        self.threshold = threshold
        self.grid_size = grid_size
        self.mean = 0
        self.std = 0
        self.bound = None
        self.cMap = None
        self.norm = None
        self.timer = True
        self.itinerary = 0
        self.start = []
        self.end = []
        self.xy_coord = []
        self.grid_count = []
        self.xs = np.arange(-73.59, -73.5501, self.grid_size)
        if self.grid_size == 0.002:
            self.ys = np.arange(45.528, 45.488, -self.grid_size)
        if self.grid_size == 0.001:
            self.ys = np.arange(45.529, 45.488, -self.grid_size)
        self.get_crime_data(threshold, grid_size)
        self.color_map()
        self.draw_grid()
        self.crime_plot()

    def get_crime_data(self, threshold, grid_size):
        # Use np.histogram2d to arrange each cell with the murder count
        histogram_array = np.histogram2d(self.shape_points[:, 0], self.shape_points[:, 1],
                                         bins=20 if grid_size == 0.002 else 40)
        crime_array = np.flip(np.sort(histogram_array[0].flatten(), axis=0))
        if grid_size == 0.002:
            self.bound = [crime_array[int((400 * (1 - (threshold / 100))) - 1)]]
        elif grid_size == 0.001:
            self.bound = [crime_array[int((1600 * (1 - (threshold / 100))) - 1)]]
        self.mean = np.mean(crime_array)
        self.std = np.std(crime_array)

    def color_map(self):
        cMap = plt.cm.jet
        cMapList = [(.4, .1, .6, 1.0), (1, 0.9, 0., 1.0)]
        self.cMap = mpl.colors.LinearSegmentedColormap.from_list(
            'Custom cMap', cMapList, cMap.N)
        self.norm = mpl.colors.BoundaryNorm(self.bound, cMap.N)

    def draw_grid(self):
        for y in range(len(self.ys)):
            for x in range(len(self.xs)):
                self.xy_coord.append([round(self.xs[x], 3), round(self.ys[y], 3)])
        self.xy_coord = np.asarray(self.xy_coord)

    @staticmethod
    def timeout(self):
        self.time = False
        print("Time is Up. The optimal path is not found")

    def __onclick__(self, click):
        if self.grid_size == 0.002:
            s = 300
        else:
            s = 100
        if click.xdata is not None:
            if self.itinerary == 0:
                for x in self.xy_coord:
                    if 0 <= (click.xdata - x[0]) < self.grid_size and 0 <= (click.ydata - x[1]) < self.grid_size:
                        self.start = [x[0], x[1]]
                        plt.scatter(x[0], x[1], marker=".", color="red", s=s)
            if self.itinerary == 1:
                t = Timer(10, self.timeout, args=[self])
                for x in self.xy_coord:
                    if 0 <= (click.xdata - x[0]) < self.grid_size and 0 <= (click.ydata - x[1]) < self.grid_size:
                        self.end = [x[0], x[1]]
                        plt.scatter(x[0], x[1], marker="*", color="red", s=s)
                        t.start()
                        # Get path
                        self.path = PathGenerator.a_star(PathGenerator(self.grid_size, self.grid_count, self.bound),
                                                             self.start,
                                                             self.end)
                        if self.path is not False:
                            print("Path Found")
                            t.cancel()
                            # Plot path on the graph
                            for i in range(len(self.path) - 1):
                                plt.plot((self.path[i].location[0], self.path[i + 1].location[0]),
                                         (self.path[i].location[1], self.path[i + 1].location[1]), '-')
                        elif self.path is False:
                            t.cancel()
                            print("Due to blocks, no path is found. Please Change the map and try again")

            self.itinerary += 1
        plt.show()

    def crime_plot(self):
        fig, ax = plt.subplots(figsize=(8, 8))
        plt.title("Threshold: " + str(float(self.threshold)) + "%   Grid Size: " + str(self.grid_size)
                  + "   Mean: " + str(self.mean) + "   Std: " + str(self.std))

        ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
        histogram = plt.hist2d(self.shape_points[:, 0], self.shape_points[:, 1],
                               bins=20 if self.grid_size == 0.002 else 40,
                               cmap=self.cMap, norm=self.norm)

        # Here i am only arrange the data in a more accessible way so i can easily determine the neighbours.
        # To see how it looks like, just print self.grid_count
        histogram = np.flip(np.transpose(histogram[0]), axis=0)
        if self.grid_size == 0.002:
            for x in range(0, 400):
                self.grid_count.append(
                    [self.xy_coord[x][0], self.xy_coord[x][1], int(histogram[floor(x / 20)][(x % 20)])])
                plt.text(self.xy_coord[x][0] + 0.0005, self.xy_coord[x][1] + 0.0007,
                         str(int(histogram[floor(x / 20)][(x % 20)])),
                         fontsize=8)
            self.grid_count = np.asarray(self.grid_count)

        if self.grid_size == 0.001:
            for x in range(0, 1600):
                self.grid_count.append(
                    [self.xy_coord[x][0], self.xy_coord[x][1], int(histogram[floor(x / 40)][(x % 40)])])
                plt.text(self.xy_coord[x][0] + 0.0002, self.xy_coord[x][1] + 0.00035,
                         str(int(histogram[floor(x / 40)][(x % 40)])),
                         fontsize=5.5)
            self.grid_count = np.asarray(self.grid_count)
        fig.canvas.mpl_connect('button_press_event', self.__onclick__)
        plt.show()
