# -*- coding:utf-8 -*-
from colorama import Fore, Style


def before_feature(context, feature):
    print('----------------------------------------------------------')
    print(('feature: ' + Fore.GREEN + '{}' + Style.RESET_ALL).format(feature.name))


def before_scenario(context, scenario):
    print('==========================================================')
    print(("For scenario: " + Fore.YELLOW + "{}" + Style.RESET_ALL).format(scenario.name))
    print('==========================================================')


def after_scenario(context, scenario):
    print('**********************************************************')
    print(("time consuming: " + Fore.BLUE + "{}" + Style.RESET_ALL).format(scenario.duration))
    print('**********************************************************')


def after_feature(context, feature):
    print((
            'time consuming of feature ' + Fore.GREEN + '{}' + Style.RESET_ALL + ': ' + Fore.BLUE + '{}' + Style.RESET_ALL).format(
        feature.name, feature.duration))
    print('----------------------------------------------------------')
