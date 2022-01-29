# %% 
#Drug Analyzer 

class DrugsAnalyzer:
    def __init__ (self, data):
        self.data = data 


    def __add__(self, data):
        if len(data) == 4:
            if all(isinstance(i, float) for i in data[1:]) and isinstance(data[0],str):
                self.data = self.data + [data]
                return self 
            else:
                raise ValueError('Improper type on list added')
        else:
            raise ValueError("Improper lengh on list added")


# %%
my_drug_data = [
...                 ['L01-10', 1007.67, 102.88, 1.00100],
...                 ['L01-06', 996.42, 99.68, 2.00087],
...                 ['G02-03', 1111.95, 125.04, 3.00100],
...                 ['G03-06', 989.01, 119.00, 4.00004]
... ]

my_analyzer = DrugsAnalyzer(my_drug_data)


# %%
my_analyzer = my_analyzer + ['G03-01', 789.01, 129.00, 0.00008]
print (my_analyzer)

# %%
