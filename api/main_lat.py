import os
import re
import sys
sys.path.append("api/calculation/src/")
from calculation.src.airplane import Airplane
import json

def process_data():

    try:
        # Read the contents of the latMatrix.json file
        with open("latMatrix.json", "r") as f:
            matrix_content = json.load(f)

        # Return the file in the response
        return {
            "success": True,
            "data": matrix_content,
            "headers": {
                "Content-Disposition": f"attachment; filename={os.path.basename('latMatrix.json')}",
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        print("Error:", e)
        return {"success": False, "error": "Vérifier que les fichiers sont bien au bon format et dans le bon ordre. Voir README.md"}


# create function that put aircraft matrix and control matrix in a txt file

def write_matrix(aircraft_matrix, control_matrix):
    # Write both matrices to a JSON file
    with open("latMatrix.json", "w") as f:
        matrix = {
            "aircraft_matrix": aircraft_matrix.tolist(),
            "control_matrix": control_matrix.tolist()
        }

        json.dump(matrix, f)

def replacer(data_file):
    data_file = re.sub(r'\s+', '', data_file)
    return data_file


# collect sys arg as a string
data_str1 = sys.argv[1] # latgitudinalSD.json
data_str2 = sys.argv[2] # flightConditions.json


data_str1 = data_str1.replace('\\r', '').replace('\\n', ''). replace(' ', '').replace('\\', '')
data_str2 = data_str2.replace('\\r', '').replace('\\n', ''). replace(' ', '').replace('\\', '')

# remove any extra spaces
data_str1 = replacer(data_str1)
data_str2 = replacer(data_str2)

# match exactly if there is a ',n'
data_str1 = re.sub(r',n', ',', data_str1)
data_str2 = re.sub(r',n', ',', data_str2)

# match exactly if there is a 'r,'
data_str1 = re.sub(r',r', ',', data_str1)
data_str2 = re.sub(r',r', ',', data_str2)


# do something with file1 and file2
print(f"Contents of file1: {data_str1}")
print(f"Contents of file2: {data_str2}")


data = [data_str2, data_str1]

# open geometricData/geometric.json
with open("calculation/flights/geometricData/geometric.json", "r") as f:
    geometric_content = json.load(f)

S = geometric_content["S"]["value"]  # Wing area
A = geometric_content["AR"]["value"]  # Aspect ratio
lambda_ = 0.5  # Taper ratio
b = geometric_content["b"]["value"]  # Wingspan
c_mean = geometric_content["c"]["value"] # Mean chord
e = geometric_content["e"]["value"]  # Oswald factor

# CAUTION
# IF YOU WANT TO USE THE DEFAULT FILES, JUST PUT "None" FOR THE LAST ARGUMENT
airplane = Airplane("Business JET", S, A, lambda_, b, c_mean, e, "lateral", data)


print("================================")

print("Aircraft matrix for longitudinal stability:\n")
airplane.get_lateral_aircraft_matrix()
print(airplane.aircraft_matrix)

print("================================")

print("Control matrix (Rudder/Throttle) for lateral stability")
airplane.get_lateral_control_matrix()
print(airplane.control_matrix)

print("================================")

print("Eigen values:")
airplane.set_lateral_eigenvalues()
airplane.set_lateral_eigenvectors()
airplane.set_lateral_characteristic_equation()
print(airplane.get_lateral_eigenvalues())
poly = airplane.get_lateral_characteristic_equation()
print("\nLateral Characteristic equation:")
for i in range(len(poly) - 1):
    print(abs(poly[-1 - i]), "* s^", len(poly) - i - 1, " + ", end="")
print(abs(poly[0]))
print("================================")


# print("--------------------------------")
#
# print("Exemple to get a cruise condition")
# print("U0 = ", airplane.get_cruise_condition("V"))
#
# print("--------------------------------")


# print("Parameters")
# params = ["Xu", "Xw", "Zu", "Zw", "Zw_dot", "Zq", "Mu", "Mw", "Mw_dot", "Mq"]
# for param in params:
#     print(param, " = ", getattr(airplane, param))
# print("--------------------------------")


TFs = airplane.set_lateral_transfer_functions()

print(f"Transfer functions for Aileron:\n")
fct_name = ["u(s)/delta_a(s)", "w(s)/delta_a(s)", "q(s)/delta_a(s)", "theta(s)/delta_a(s)"]
for i, tf in enumerate(TFs["aileron"]):
    print(f"{i}->{fct_name[i]}:\n {tf}")
    print("\n")

print(f"Transfer functions for Rudder:\n")
fct_name = ["u(s)/delta_r(s)", "w(s)/delta_r(s)", "q(s)/delta_r(s)", "theta(s)/delta_r(s)"]
for i, tf in enumerate(TFs["rudder"]):
    print(f"{i}->{fct_name[i]}:\n {tf}")
    print("\n")
print("================================")

# airplane.lat_plot_stability("Rolling")
# airplane.lat_plot_stability("Spiral")
# airplane.lat_plot_stability("Dutch Roll")

# #
data = airplane.lat_plot_stability("Rolling")
print(f"ImageDataRolling<{data}>Rolling")
data2 = airplane.lat_plot_stability("Spiral")
print(f"ImageDataSpiral<{data2}>Spiral")
data3 = airplane.lat_plot_stability("Dutch Roll")
print(f"ImageDataDutchRoll<{data3}>DutchRoll")



# write_matrix(airplane.aircraft_matrix, airplane.control_matrix)

# process_data()






