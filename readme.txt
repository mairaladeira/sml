Incremental Learning of Relational Action Theories
DMKM - Symbolic Learning Project
Group: Humberto Gonzalez
	   Maira Machado Ladeira

Description: Python implementation of the IRALe algorithm for incremental learning of relational rules used in a colored world block environment.


Observations:
The definition of wellformed rules in the project file is different from the definition in the article. For this project, we use the definition present in the article.
The model class getUncovEx(self, rule) does not need the rules as a parameter and for this reason, the parameter was removed.
specialize(self, rule) method in Model class was changed to specialize(self, ex) because the specialization of the model is made against an example as in the generalization method of the same class.
specialize(self, ex) method was added to the Rule class. This method returns the specialization of the rules such that it no longer prematches example ex.
For the episode and step arguments (es, ts), we consider that each episode es will perform maximum  ts steps trying to achieve the goal
The program considers a SUCCESS state any state that contains the goal.



How to run:
This project should be executed with python version 2, operational system: Linux or Mac OS.
Command for executing the program:
python Agent.py -es <episode_size> -ts <total_steps>