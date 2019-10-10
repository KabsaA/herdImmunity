class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''
    def __init__(self, file_name):
        # TODO:  Finish this initialization method. The file_name passed should be the
        # full file name of the file that the logs will be written to.
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        self.pop_size = pop_size
        file = open(self.file_name, 'w')
        file.write("Population: " + str(pop_size)+ " Percentage: "
        + str(vacc_percentage)+ " Name of : " + str(virus_name)+ " Mortality: " + str(mortality_rate)+ "Repro Num: " + str(basic_repro_num))
        file.close()

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects {random_person.ID} \n"

        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
        file = open(self.file_name, 'a')
        if did_infect == True:
            file.write((f"{person._id} infects {random_person._id}\n"))
        elif random_person_vacc == True and did_infect == None:
            file.write((f"{person._id} didn't infect {random_person._id} because vaccinated\n"))
        elif random_person_sick == True and did_infect == None:
            file.write((f"{person._id} didn't infect {random_person._id} because already sick\n"))
        else:
            file.write((f"{person._id} didn't infect {random_person._id}\n"))

        file.close()

    def log_infection_survival(self, person, did_die_from_infection):

        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        file = open(self.file_name,"a")
        if did_die_from_infection:
            file.write(f"{person._id} died from infection\n")
        else:
            file.write(f"{person._id} survived the infection\n")
        file.close()

    def log_time_step(self, time_step_number):
        #stretch
        # TODO: Finish this method. This method should log when a time step ends, and a
        # new one begins.
        # NOTE: Here is an opportunity for a stretch challenge!
        pass
