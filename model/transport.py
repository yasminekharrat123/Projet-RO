from gurobipy import Model, GRB, quicksum


def run_transport_model(origins, destinations,modes, capacities, costs,demand,supply):
    try:
        # Example data setup
        # origins = ['A', 'B']
        # destinations = ['1', '2']
        # modes = ['Road', 'Rail']
        # costs = {('A', '1', 'Road'): 2, ('A', '2', 'Road'): 3,
        #          ('B', '1', 'Rail'): 4, ('B', '2', 'Rail'): 1}
        # capacities = {('A', '1', 'Road'): 100, ('A', '2', 'Road'): 80, ('B', '1', 'Rail'): 70, ('B', '2', 'Rail'): 90}
        # demand = {'1': 50, '2': 60}
        # supply = {'A': 80, 'B': 90}

        # Initialize model
        model = Model("Transportation Model")

        # Decision variables
        x = {}
        for i in origins:
            for j in destinations:
                for m in modes:
                    x[(i, j, m)] = model.addVar(
                        vtype=GRB.CONTINUOUS, name=f"x_{i}_{j}_{m}")

        # Objective function
        model.setObjective(
            quicksum(costs[i, j, m] * x[i, j, m] for i, j, m in x.keys()), GRB.MINIMIZE)

        # Constraints
        # Supply constraints
        for i in origins:
            model.addConstr(quicksum(x[i, j, m] for j in destinations for m in modes if (
                i, j, m) in x) <= supply[i], f"supply_{i}")

        # Demand constraints
        for j in destinations:
            model.addConstr(quicksum(x[i, j, m] for i in origins for m in modes if (
                i, j, m) in x) >= demand[j], f"demand_{j}")

        # Capacity constraints
        for i, j, m in capacities:
            model.addConstr(x[i, j, m] <= capacities[i, j, m],
                            f"cap_{i}_{j}_{m}")

        # Solve the model
        model.optimize()

        # Check if a solution exists
        if model.status == GRB.OPTIMAL:
            print("Optimal solution found:")
            for v in model.getVars():
                if v.X > 0:
                    print(f"{v.VarName} = {v.X}")
            print(f"Total minimized cost: {model.ObjVal}")
        else:
            print("No optimal solution found")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    run_transport_model()
