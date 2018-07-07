#!/usr/bin/env python

#-*- encoding: utf-8 

'''
                      ______   ___  __
                     / ___\ \ / / |/ /
                    | |    \ V /| ' / 
                    | |___  | | | . \ 
                     \____| |_| |_|\_\
 ==========================================================================
@author: Yekun Chai

@license: School of Informatics, Edinburgh

@contact: s1718204@sms.ed.ac.uk

@file: plot_fit.py

@time: 23/06/2018 13:31 

@desc：       
               
'''

from settings import *

import os
import matplotlib.pyplot as plt
import pandas as pd

from keras.utils import plot_model


def plot_fit(history, plot_filename):
    assert len(history.history) == 4, "Error: did not fit validation data!"
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(loss) + 1)

    plt.figure(figsize=(16, 4))
    plt.subplot(121)
    # "bo" is for "blue dot"
    plt.plot(epochs, loss, 'r', label='Training loss')
    # b is for "solid blue line"
    plt.plot(epochs, val_loss, 'g--', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid()

    plt.subplot(122)
    # "bo" is for "blue dot"
    plt.plot(epochs, acc, 'b', label='Training acc')
    # b is for "solid blue line"
    plt.plot(epochs, val_acc, 'y--', label='Validation acc')
    plt.title('Training and validation acc')
    plt.xlabel('Epochs')
    plt.ylabel('Acc')
    plt.legend()
    plt.grid()
    save_fig(plt, plot_filename=plot_filename)
    # plt.show()


def save_fig(plt, plot_filename, plot_dir=plot_dir):
    print("plot_dir:", plot_dir)
    if not os.path.exists(plot_dir):
        os.mkdir(plot_dir)
    filename = os.path.join(plot_dir, plot_filename)
    plt.savefig('{}'.format(filename))
    print('{} saved!'.format(filename))


def visialize_model(model, filepath):
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
    filename = os.path.join(model_dir, filepath)
    # visualize model
    plot_model(model, filename, show_shapes=True)
    print("Plot model graph to {}".format(filename))


def save_history(history, csv_name, subdir=False):
    assert csv_name[-4:] == '.csv', "Error: didnot give a valid csv_name!"
    if not os.path.exists(history_dir):
        os.mkdir(history_dir)
    if subdir is not False:
        subdir = os.path.join(history_dir, subdir)
        if not os.path.isdir(subdir):
            os.mkdir(subdir)
        csv_file = os.path.join(subdir, csv_name)
        # =========================
        # 1. save to txt
        # with open(filename, 'w') as f:
        #     f.write(str(history))
        # ==========================
        hist = pd.DataFrame.from_dict(history.history, orient='columns')
        hist.to_csv(csv_file)
        print('History is written into {}'.format(csv_file))
        print('-' * 80)


def plot_all_history(subdir, plot_filename='default.pdf', figsize=(16, 9)):
    subdir = os.path.join(history_dir, subdir)
    assert os.path.isdir(subdir) == True, "Error: {} does not exists!".format(subdir)

    sum_plot = os.path.join(history_dir, 'plot_all')
    if not os.path.isdir(sum_plot):
        os.mkdir(sum_plot)

    # set color list
    # colors = [c for c in list(matplotlib.colors.cnames.keys()) if not c.startswith('light')]
    colors = ['green', 'red', 'blue', 'goldenrod', 'black', 'lime', 'cyan', 'chartreuse', 'yellow', 'm', 'purple',
              'olive', 'salmon', 'darkred', 'pink']
    markers = ['d', '^', 's', '*']

    plt.figure(figsize=figsize)
    plt.subplot(121)
    for i, filename in enumerate(os.listdir(subdir)):
        if filename[-4:] != '.csv': continue
        line_label = filename[:-4]
        csv_file = os.path.join(subdir, filename)
        history = pd.read_csv(csv_file)
        # plot val and acc loss
        loss = history['loss']
        val_loss = history['val_loss']
        epochs = range(1, len(loss) + 1)

        plt.plot(epochs, loss, color=colors[i % len(colors)], linestyle='-', marker=markers[i % len(markers)],
                 label='{} training loss'.format(line_label))
        plt.plot(epochs, val_loss, color=colors[i % len(colors)], marker=markers[i % len(markers)], linestyle='dashed',
                 label='{} validation loss'.format(line_label))
    plt.title('Training and validation loss', fontsize='25')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    # plt.grid()
    plt.legend()
    plt.grid()
    # =============================
    # plot acc
    plt.subplot(122)
    for i, filename in enumerate(os.listdir(subdir)):
        if filename[-4:] != '.csv': continue
        csv_file = os.path.join(subdir, filename)
        history = pd.read_csv(csv_file)
        line_label = filename[:-4]
        acc = history['acc']
        val_acc = history['val_acc']
        epochs = range(1, len(acc) + 1)
        # plot acc
        plt.plot(epochs, acc, color=colors[i % len(colors)], marker=markers[i % len(markers)], linestyle='-',
                 label='{} training acc'.format(line_label))
        plt.plot(epochs, val_acc, color=colors[i % len(colors)], marker=markers[i % len(markers)], linestyle='dashed',
                 label='{} validation acc'.format(line_label))
        plt.title('Training and validation acc', fontsize='25')
    plt.xlabel('Epochs')
    plt.ylabel('Acc')
    plt.legend()
    plt.grid()

    save_fig(plt, plot_filename=plot_filename, plot_dir=sum_plot)
    print("{} saved!".format(plot_filename))
    print('-' * 80)

    plt.show()


# def visulize_embedding()


if __name__ == "__main__":
    # save_history({'val_acc':[1,1], 'val_loss':[2,3], 'acc':[3,3], 'loss':[5,3]}, 'val1.csv', 'val')
    # history = 'history example'
    # use example
    # save_history(history, 'train_val.csv', subdir='val')

    # subdir = 'dir to save csv'
    subdir = 'CNN_glove50'
    #    subdir='lstm+cnn_char'
    plot_all_history(subdir, plot_filename='%s.pdf' % subdir, figsize=(60, 30))
