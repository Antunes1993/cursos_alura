import time 
import threading

#Basic thread
done = False 
def simulation_process(simulation_input, simulation_input_2):
    counter = 0
    while not done: 
        time.sleep(1)
        counter +=1
        print(f"Running Simulation... {counter} ----> {simulation_input} // {simulation_input_2}")

threading.Thread(target=simulation_process, args=(6, 30)).start()
threading.Thread(target=simulation_process, args=(5, 50)).start()

input("press enter to quit") 
done = True

