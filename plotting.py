#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 11:55:48 2020

@author: florian
"""
import os
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns

def generate_ROC_curve(model, X_test, y_test, comparison):
    print("Generating ROC")
    file = os.path.join("Plots","ROC_Curve", f"{comparison}.png")
    y_pred_proba = model.predict_proba(X_test)[:,1]
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    # Plot ROC curve
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr, tpr)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.savefig(file)
    plt.close()

def auto_pct(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d})".format(pct, absolute)

def generate_piechart_legend(data, labels, title, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)    
    fig, ax = plt.subplots(figsize=(9, 4), subplot_kw=dict(aspect="equal"))
    # autopct=lambda pct: auto_pct(pct, data)
    
    wedges, texts, autotexts = ax.pie(
        data,
        autopct='%1.1f%%',
        textprops=dict(color="black"),
        colors = plot_colors)
    
    ax.legend(wedges, labels,
          title="Réponses",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1),
          prop={'size': 8})

    plt.setp(autotexts, size=8, weight="bold")
    if title:
        ax.set_title(title)
    plt.tight_layout()
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close()

def donut(data, labels, title, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)    
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    data_in_percentage = 100 * np.array(data)/sum(data)
    wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)
    
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")
    
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        
        elts_of_text = [str(round(data_in_percentage[i],2)) + "%",
                        f"({data[i]}) :", labels[i]]
        text = " ".join(elts_of_text)
        ax.annotate(text, xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw)
    if title:
        ax.set_title(title)
    
    plt.tight_layout()
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close()

def histogram(df, title, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)    
    fig, ax = plt.subplots(figsize=(9, 9))    
    df.plot.bar(y=df)
    if title:
        ax.set_title(title)
    ax.set_ylabel("Total")
    plt.tight_layout()
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close()

def generate_piechart_no_legend(df, title, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 4))
    df.plot.pie(y=df, autopct='%1.1f%%', colors = plot_colors)
    if title:
        plt.title(title)
    ax.set_ylabel('')
    ax.set_xlabel('')
    plt.tight_layout()
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close()

def generate_heatmap(contigency_table, comparison, p_value):
    plot_dir = os.path.join("Plots", "Chi_square_heatmaps_percentage_corrected")
    code = comparison.split("_")[0]
    title = code_question[code]
    split_title = title.split(" ")
    enter_line = 8
    for l in range(enter_line,len(split_title),enter_line):
        split_title.insert(l,"\n")
    split_title.append("\n")
    split_title.append(f'p_value ={round(p_value,4)}')
    new_title = " ".join(split_title)
    significant_dir = os.path.join(plot_dir, "Significant")
    non_significant_dir = os.path.join(plot_dir, "Not_significant")
    os.makedirs(significant_dir, exist_ok=True)
    os.makedirs(non_significant_dir, exist_ok=True)
    if p_value <= 0.05:
        heatmap_file = os.path.join(significant_dir, comparison +".png")
    else:
        heatmap_file = os.path.join(non_significant_dir, comparison +".png")   
    fig, ax = plt.subplots()
    fig.set_size_inches(12,8)
    sns.heatmap(contigency_table, annot=True, cmap="RdBu", square=True,
                annot_kws={"fontsize":30, "color":"black"})
    # plt.title(new_title, size=20)
    plt.tight_layout()
    plt.savefig(heatmap_file, dpi=300, bbox_inches='tight')
    plt.clf()
    plt.close()

  
