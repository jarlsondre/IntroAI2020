import copy
import itertools


class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        self.backtrack_called = 0
        self.backtrack_returned_failure = 0

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [(i, j) for i in self.constraints for j in self.constraints[i]]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [(i, var) for i in self.constraints[var]]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = list(filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j]))

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.

        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """
        # TODO: IMPLEMENT THIS
        self.backtrack_called += 1  # Øker telleren på hvor mange ganger backtrack blir kalt
        var = self.select_unassigned_variable(assignment)  # Velger en variabel som har flere mulige verdier

        if var == "":  # Dersom True vil alle variabler har en fastsatt verdi og dermed har vi en løsning. Denne returneres
            return assignment

        # Dersom vi ikke har en løsning:
        for value in assignment[var]:  # Vi prøver alle mulige lovlige verdier for denne variabelen
            assigment_copy = copy.deepcopy(assignment)  # Lager en kopi slik at vi ikke endrer originalen
            assignment[var] = value  # Setter verdien til variabelen til value for å se om det er riktig verdi

            if self.inference(assignment, self.get_all_neighboring_arcs(var)):  # Dersom inference returnerer False vet vi at dette var feil løsning
                # Nå kjører vi løkken på nytt med den nye listen over lovlige elementer. Nå har vi satt en verdi
                result = self.backtrack(assignment)
                if result != -1:  # Hvis result == -1 har vi ingen løsning.
                    return result

            assignment = assigment_copy  # Dersom vi har kommet oss hit så betyr det at vi har feilet på et steg i prosessen, så vi resetter og prøver neste mulige verdi for variabelen
        self.backtrack_returned_failure += 1  # Dersom backtrack ikke fant noen løsning så øker vi failure-counteren
        return -1  # Returner hvis vi ikke har en løsning

    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """
        # TODO: IMPLEMENT THIS
        # Returnerer den første variabelen som her flere mulige verdier.
        for i in self.variables:
            if len(assignment[i]) > 1:
                return i
        return ""  # Hvis det ikke finnes flere variabler uten verdi returners ""

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        # TODO: IMPLEMENT THIS
        while queue:  # Løkken skal iterere så lenge det er elementer igjen i køen
            tmp = queue.pop(0)  # Vi tar ut det første elementet på formen ('x1-y1', 'x2-y2')
            i = tmp[0]  # Setter denne lik 'x1-y1'
            j = tmp[1]  # Setter denne lik 'x2-y2'
            if self.revise(assignment, i, j):  # Hvis vi klarte å revise mhp. 'x1-y1', altså fantes det noen "lovlige" verdier for i som viste seg å ikke være lovlige like vel?
                if len(assignment[i]) == 0:  # Sjekker om det ikke finnes noen lovlige verdier for i, returnerer False hvis det er tilfellet
                    return False

                tmp = self.get_all_neighboring_arcs(i)  # Setter tmp lik listen med alle constraints som hører til variabelen i
                tmp.remove((j, i))  # Fjerner (j, i) siden vi allerede har "revised" mhp denne
                for k in tmp:
                    queue.append(k)  # For alle constraints til variabelen i vil vi revise, så disse legges til i køen.
                    # Dersom noe allerede har blitt revised, vil det bli forsøkt revised på nytt. Dette vil returnere False hvis man ikke fikk gjort noe med den, og da legges den ikke til igjen
        return True

    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """
        # TODO: IMPLEMENT THIS
        revised = False
        for x in assignment[i]:  # Går gjennom mulige verdier for i.
            var = False
            for y in assignment[j]:  # Går gjennom mulige verdier for j.
                if (x, y) in self.constraints[i][j]:
                    var = True  # Setter var = True hvis det finnes en verdi y for x slik at constrains er oppfylt.
                    break
            if not var:
                # Hvis ikke constrains er mulig å oppfylt for x, fjernes x fra mulige verdier for i.
                assignment[i].remove(x)
                revised = True
        return revised  # Returner True hvis den har fjernet en verdi, False hvis ikke.


def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    edges = {'SA': ['WA', 'NT', 'Q', 'NSW', 'V'], 'NT': ['WA', 'Q'], 'NSW': ['Q', 'V']}
    colors = ['red', 'green', 'blue']
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp


def create_sudoku_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    board = list(map(lambda x: x.strip(), open(filename, 'r')))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), list(map(str, range(1, 10))))
            else:
                csp.add_variable('%d-%d' % (row, col), [board[row][col]])

    for row in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for col in range(9)])
    for col in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for row in range(9)])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp


def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            if len(solution['%d-%d' % (row, col)]) == 1:
                print(solution['%d-%d' % (row, col)][0], " ", end=""),
            else:
                print(0, end=""),
            if col == 2 or col == 5:
                print('|', " ", end=""),
        print("")
        if row == 2 or row == 5:
            print('---------+-----------+---------')


easy = create_sudoku_csp("easy.txt")
medium = create_sudoku_csp("medium.txt")
hard = create_sudoku_csp("hard.txt")
very_hard = create_sudoku_csp("veryhard.txt")

#
# print(f"get_all_arcs gir ut alle de forskjellige rutene (variables) som kan komme i konflikt \n"
#       f"dvs de som er i samme vertikale linje, horisontale linue eller i samme box på hele brettet \n")
# print(easy.get_all_arcs(), "\n")
# print(easy.get_all_neighboring_arcs("0-0"), "\n")




print('---------+---EASY----+---------')
print_sudoku_solution(easy.backtracking_search())
print(f'Backtracked called: {easy.backtrack_called}, Backtracked failure: {easy.backtrack_returned_failure}')
print()
print()

print('---------+--MEDIUM---+---------')
print_sudoku_solution(medium.backtracking_search())
print(f'Backtracked called: {medium.backtrack_called}, Backtracked failure: {medium.backtrack_returned_failure}')
print()
print()

print('---------+---HARD----+---------')
print_sudoku_solution(hard.backtracking_search())
print(f'Backtracked called: {hard.backtrack_called}, Backtracked failure: {hard.backtrack_returned_failure}')
print()
print()

print('---------+-VERY-HARD-+---------')
print_sudoku_solution(very_hard.backtracking_search())
print(f'Backtracked called: {very_hard.backtrack_called}, Backtracked failure: {very_hard.backtrack_returned_failure}')
print()
print()




