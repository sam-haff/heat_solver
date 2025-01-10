The following examples work given you have a copy of the package in your current working directory\
\
**Example**(2D surface heating process due to the boundaries beign hotter than the last of the surface) 
```
python -m heat_solver --k 0.5 --iters_per_vis 50 --num_vis 10 simulate2D --x_grid 30 --y_grid 30 --extent_x 100 --extent_y 60 --T_left 150 --T_right 30 --T_top 300 --T_bot 150 --T_mid 30
```
|100 seconds|350 seconds|
|--- | --- |
|![Figure_4](https://github.com/user-attachments/assets/44d9897b-a348-4678-8d83-be0dc079600c)|![Figure_1](https://github.com/user-attachments/assets/c2218470-fefb-47d2-bd92-2328d6225ced)|

\
\
**Example**(1D surface cooling process due to the boundaries beign colder than the rest of the surface)
```
python -m heat_solver simulate1D
```
In that case, you will be prompted(in human readable form) to enter all the required parameters(same is possible with *simulate2D* cli command)
![image](https://github.com/user-attachments/assets/fc73261b-7819-4635-b1dd-1488372ad4a2)
|100 seconds|500 seconds|
| --- | --- |
|![Figure_2](https://github.com/user-attachments/assets/330a99e5-2b25-4666-9aa3-319e7baed806)|![Figure_3](https://github.com/user-attachments/assets/4dea9c06-290e-4e5c-80ca-13743eb0c2dd)|
