"""
Coded by: RONGERE Julien

This module contains the fram where the user can evaluate a model and displays the different metrics of the model on the test set


"""

#------------Imports begin------------
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import tkinter.ttk as ttk
from tkinter import messagebox

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score