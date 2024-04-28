from gurobipy import Model, GRB, quicksum


def run_crew_scheduling_model(crew, flights, qualifications, costs):
    try:
        # Example data setup
        # crew = ['Pilot1', 'Pilot2']
        # flights = ['Flight1', 'Flight2']
        # qualifications = {('Pilot1', 'Flight1'): True, ('Pilot2', 'Flight2'): True}
        # costs = {('Pilot1', 'Flight1'): 100, ('Pilot2', 'Flight2'): 120}

        # Initialize model
        model = Model("Crew Scheduling Model")

        # Decision variables
        y = {}
        for c in crew:
            for f in flights:
                y[(c, f)] = model.addVar(vtype=GRB.BINARY, name=f"y_{c}_{f}")

        # Objective function
        model.setObjective(quicksum(costs.get((c, f), 0) * y[c, f] for c in crew for f in flights), GRB.MINIMIZE)

        # Constraints
        # Crew must be qualified for the flights they are assigned to
        for c, f in qualifications:
            if not qualifications[c, f]:
                model.addConstr(y[c, f] == 0, f"qual_{c}_{f}")

        # Each flight needs at least one pilot
        for f in flights:
            model.addConstr(quicksum(y[c, f] for c in crew if (c, f) in qualifications) >= 1, f"crew_for_{f}")

        # Solve the model
        model.optimize()

        # Display results
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
