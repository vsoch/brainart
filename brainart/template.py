#!/usr/bin/python

from brainart.utils import get_packagedir
base = get_packagedir()

def get_template(template_name,ext="html"):
    '''get_template
    :param template_name: name of template (without suffix) to get in the template package folder
    :param ext: extension of template (default is html)
    '''
    template_file = "%s/templates/%s.%s" %(base,template_name,ext)
    filey = open(template_file,"r")
    template = "\n".join(filey.readlines())
    filey.close()
    return template


def sub_template(template,template_tag,substitution):
    '''sub_template
    make a substitution for a template_tag in a template
    :param template: the template, read in as a str
    :param template_tag: the tag in the template, surrounded with {{}}
    :param substitution: the text (str) to substitute with
    '''
    template = template.replace("{{%s}}" %template_tag,substitution)
    return template

def save_template(output_file,html_snippet):
    '''save_template
    :param output_file: the output file to save the template to
    :param html_snippet: the template text to save
    '''
    filey = open(output_file,"w")
    filey.writelines(html_snippet)
    filey.close()
