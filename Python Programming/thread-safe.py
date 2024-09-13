
import time 
import threading

'''
To allow user_input variables to be modified by user during the simulation, you'll need 
to use a thread-safe mechanism to update these values. 

One common way to do that is by 
using a threading.lock to manage access to shared variables and make sure updates are 
sincronized accross threads.
'''
#Global variables - can be accesed and modified from multiple threads.
done = False 
simulation_input = 6 
simulation_input_2 = 30 

#Lock for synchronizing access to shared variables
#This ensure that changes to the simulation variables are safely updated and 
#accessed by the simulation_process function.
lock = threading.Lock()

#simulation process
def simulation_process():
    global simulation_input, simulation_input_2, done
    counter = 0 
    while not done: 
        time.sleep(1)
        counter += 1 
        with lock:
            print(f"Running simulation... {counter} ---> {simulation_input} // {simulation_input_2}")

# Start the simulation process in a separate thread
thread = threading.Thread(target=simulation_process)
thread.start()

#The main thread continuously prompts the user to enter new values for simulation inputs
try:
    while not done:
        # Get user input
        new_input = input("Enter new value for simulation_input (or 'exit' to stop): ")
        if new_input.lower() == 'exit':
            done = True
            break
        try:
            new_input = int(new_input)
            with lock:
                simulation_input = new_input
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

        new_input_2 = input("Enter new value for simulation_input_2 (or 'exit' to stop): ")
        if new_input_2.lower() == 'exit':
            done = True
            break
        try:
            new_input_2 = int(new_input_2)
            with lock:
                simulation_input_2 = new_input_2
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

finally:
    # Ensure that the thread has finished before exiting
    done = True
    thread.join()
    

