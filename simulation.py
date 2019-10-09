import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):

    def __init__(self, pop_size, vacc_percentage, virus, initial_infected):
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.


        self.pop_size = pop_size # Int
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.virus_name = virus_name
        self.mortality_rate = mortality_rate
        self.basic_repro_num = basic_repro_num
        self.initial_infected = 1 # Int
        self.total_infected = 0 # Int
        self.total_vaccinated = 0
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.file_name = "Name:{}Population:{}Vaccinated:{}Infected:{}.txt".format(
            self.virus_name, self.pop_size, self.vacc_percentage, self.initial_infected)
        self.logger = Logger(self.file_name)
        self.newly_infected = []
        self.population = self._create_population() # List of Person objects
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus_name, self.mortality_rate, self.basic_repro_num)

    def _create_population(self, initial_infected=10):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.
            Returns:
                list: A list of Person objects.
        '''
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population that has
        # the correct intial vaccination percentage and initial infected.
        pop = []
        vacc_num = int(self.pop_size * self.vacc_percentage)
        for person_index in range(self.pop_size):
            if person_index < initial_infected:
                pop.append(Person(person_index, True))
            else:
                pop.append(Person(person_index, False))

        return pop

    def get_infected(self):
        alive_infected = []
        for person in self.population:
            if person.infection and person.is_alive:
                alive_infected.append(person)
        return alive_infected

    def _simulation_should_continue(self):
        # TODO: Complete this helper method.  Returns a Boolean.

        if self.get_infected() == (self.pop_size**0.9):
            return False
        else:
            return True


    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        # TODO: Finish this method.  To simplify the logic here, use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper
        time_step_counter = 0
        should_continue = True

        # TODO: for every iteration of this loop, call self.time_step() to compute another
        # round of this simulation.
        while should_continue:
            time_step_counter += 1
            self.time_step()
            should_continue = self._simulation_should_continue()
            self.logger.log_time_step(time_step_counter)


        print('The simulation has ended after {time_step_counter} turns.'.format(time_step_counter))


    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.
        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        # TODO: Finish this method.
        infected_total = self.get_infected()

        for person in infected_total:
            count = 0
            while count < 100:
                random_person = random.choice(self.population)
                while random_person.is_alive != True:
                    random_person = random.choice(self.population)
                self.interaction(person, random_person)
                count += 1

        for person in infected_total:
            survived = person.did_survive_infection()
            if survived == True:
                self.total_vaccinated += 1
                self.logger.log_infection_survival(person, False)
            else:
                self.total_dead += 1
                self.logger.log_infection_survival(person, True)

        self._infect_newly_infected()

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.
        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        if random_person.is_vaccinated:
            self.logger.log_interaction(person, random_person, False, True, False)
        elif random_person.infection != None:
            self.logger.log_interaction(person, random_person, True, False, False)
        else:
            ran_chance = random.random()
            if ran_chance < person.infection.repro_rate:
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person, random_person, False, False, True)
            else:
                self.logger.log_interaction(person, random_person, False, False, False)


    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for person_index_id in self.newly_infected:
            self.population[person_index_id].infection = self.virus
            self.total_infected += 1

        self.newly_infected *= 0



if __name__ == "__main__":
    params = sys.argv[1:]
    print(params)
    virus_name = str(params[2])
    basic_repro_num = float(params[4])
    mortality_rate = float(params[3])

    pop_size = int(params[0])
    vacc_percentage = float(params[1])

    initial_infected = int(params[5])
    #else:
    #    initial_infected = 1

    virus = Virus(virus_name, basic_repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    sim.run()
