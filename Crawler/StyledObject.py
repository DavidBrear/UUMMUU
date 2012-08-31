import urllib2;
import socket;
import sgmllib;
import re;
import MySQLdb;
import httplib;
#from htmlentitydefs import name2codepoint as n2cp;
import sys;
import threading;
import time;
'''
    CSSValue is a class for each of the css values
    that I am concerned with.
    the name is the property that is assigned such as background-color.
    the value is the value of this property
    the priority tells whether this should get replaced or not
        inline has highest priority
        ID has 2nd highest priorty
        CLASS has 3rd highest priorty
        CURRENT ELEMENT has 4th highest priorty
        INHERITANCE has 5th highest priority

        ** !important adds to priorty **
'''

class CSSValue():
    def __init__(self, name="", value='', priority=0):
        self.name = name;
        self.priority = priority;
        self.value = value;

# this is a prototype for the style object which should contain
# the text that a certain style is given to as well as
# the style that is applied to the given text.
class StyledObject():
    def __init__(self, text=''):
        #need to initialize all the font attributes and whether they're "important" or not.
        self.text = text.lstrip().rstrip();
        self.full_style = '';
        
        self.font = CSSValue('font', '');
        self.bgcolor = CSSValue('bgcolor','');
        self.fontsize = CSSValue('fontsize', 0);
        self.fontfam = CSSValue('fontfam', '');
        self.border = CSSValue('border', '');
        self.fontweight = CSSValue('fontweight', "");
        self.fontunder = CSSValue('fontunder', '');
        self.largestfont = 16;

    def append_text(self, text):
        self.text += re.sub(r'\s\s*', ' ', text);
        self.text = self.text.rstrip().lstrip();
        
    def add_Object(self, obj, priority=0):
        if obj:
            if self.font.value == '' or (priority >= self.font.priority and obj.font.priority != 0):
                self.font.value = obj.font.value;
                self.font.priority = priority;
            if self.bgcolor.value == '' or (priority >= self.bgcolor.priority and obj.bgcolor.priority != 0):
                self.bgcolor.value = obj.bgcolor.value;
                self.bgcolor.priority = priority;
            if self.fontsize.value == 0 or (priority >= self.fontsize.priority and obj.fontsize.priority != 0):
                self.fontsize.value = obj.fontsize.value;
                self.fontsize.priority = priority;
            if self.fontfam.value == '' or (priority >= self.fontfam.priority and obj.fontfam.priority != 0):
                self.fontfam.value = obj.fontfam.value;
                self.fontfam.priority = priority;
            if self.border.value == '' or (priority >= self.border.priority and obj.border.priority != 0):
                self.border.value = obj.border.value;
                self.border.priority = priority;
            if self.fontweight.value == '' or (priority >= self.fontweight.priority and obj.fontsize.priority != 0):
                self.fontweight.value = obj.fontweight.value;
                self.fontweight.priority = priority;
            if self.fontunder.value == '' or (priority >= self.fontunder.priority and obj.fontunder.priority != 0):
                self.fontunder.value = obj.fontunder.value;
                self.fontunder.priority = priority;
    
    def manipulate_style(self, style,  priority=0):
        '''
            This function splits the style sheet object up and finds its inner workings.
            In this function we look for specific attributes applied to the text.
            Mainly we want to know the font color, background color, font weight,
            font size and font family.
        '''
        style_split = style.split(';'); #split the attribute/value pairs from each other
        #this is a test to see if the style block ends in a semicolon. If not cut the last attribute pair off
        # it is a blank...
        if len(style_split[-1]) <= 0:
            style_split = style_split[0:-1];
        #iterate over the blocks.
        for element in style_split:
            try:
                name,value = element.split(':');
            except Exception, e:
                continue;
            value = re.sub(r'\s(\s)+', ' ', value);
            value = value.lstrip().rstrip();
            value = value.split(' ');
            name = name.lstrip().rstrip();
            important = 0;
            #check to see if this attribute is !important
            if len(value) > 1 and (value[1].lower() =='!important'):
                important = 100;
            if name == 'background-color':
                if self.bgcolor.value == '' or (priority > self.bgcolor.priority and value[0] != ''):
                    self.bgcolor.value = convert_colors(value[0].lower());
                    self.bgcolor.priority = priority;
            elif name == 'font-size':
                if self.fontsize.value == 0 or (priority > self.fontsize.priority and value[0] != ''):
                    font_val = convert_fonts(value[0]);
                    if(type(font_val) == "<type 'str'>"):
                        self.fontsize.value *= float(font_val[1:]);
                    else:
                        self.fontsize.value = font_val;
                    self.fontsize.priority = priority;
                elif isinstance(self.fontsize.value, str) and self.fontsize.value[0] == 'x':
                    font_val = convert_fonts(value[0]);
                    if (not isinstance(font_val, str)):
                       self.fontsize.value = (float(self.fontsize.value[1:])/100)*font_val; 
                    self.fontsize.priority = priority;
                    
            elif name == 'font-weight':
                if self.fontweight.value == '' or (priority > self.fontweight.priority and value[0] != ''):
                    self.fontweight.value = value[0];
                    self.fontweight.priority = priority;
            elif name == 'color':
                if self.font.value == "" or (priority > self.font.priority and value[0] != ''):
                    self.font.value = convert_colors(value[0].lower());
                    self.font.priority = priority;
            elif name == 'font-family':
                if self.fontfam.value == "" or (priority > self.fontfam.priority and value[0] != ''):
                    self.fontfam.value = value[0].split(',')[0];
                    self.fontfam.priority = priority;
            elif name == 'background':
                color = '';
                for section in value:
                    temp_color = convert_colors(section)
                    if( temp_color != ''):
                        color = temp_color;
                if(color != ''):
                    if self.bgcolor.value == '' or (priority > self.bgcolor.priority and value[0] != ''):
                        self.bgcolor.value = color;
                        self.bgcolor.priority = priority;
    '''
    # append_stylesheets addes a style sheet to the full style that is applied to this page
    '''
    def append_stylesheet(self, style, priority):
        #remove comments
        while style.find('/*') >= 0:
            comment_start = style.find('/*');
            comment_end = style.find('*/', comment_start);
            style = style[0:comment_start] + style[comment_end+2:];
        self.full_style += style;
        self.manipulate_style(style, priority);
        
'''
#convert_fonts takes in a font and spits out its value in pixels
# I chose pixels because it's the standard I use in developing webpages.
# This is the easiest way to compare word sizes.
'''
def convert_fonts(in_style):
    if re.search('^((\d)*(\.)?(\d)*)px$', in_style):
        return round((float(in_style.split('p')[0])),2);
    elif re.search('^((\d)*(\.)?(\d)*)em$', in_style):
        return round((float(in_style.split('e')[0]) * 11.7 ),2);
    elif re.search('^((\d)*(\.)?(\d)*)pt$', in_style):
        return round((float(in_style.split('p')[0]) * 1.333 ),2);
    elif re.search('^((\d)*(\.)?(\d)*)in$', in_style):
        return round((float(in_style.split('i')[0]) * 95.24 ),2);
    elif re.search('^((\d)*(\.)?(\d)*)pc$', in_style):
        return round((float(in_style.split('p')[0]) * 16 ),2);
    elif re.search('^((\d)*(\.)?(\d)*)$', in_style):
        return round(float(in_style),2);
    elif re.search('^%((\d)*(\.)?(\d)*)$',  in_style):
        return 'x'+in_style.split('%')[1];
    else:
        return 16;

'''
#convert_colors takes in a string and sees if it's a valid css color
#these colors are the most up to date Mozilla Firefox acceptable colors
#I know that there are a lot of colors that IE accepts that other browsers
#do not accept. Oh well to these. Maybe they'll be implemented later...
'''
def convert_colors(string):
    color_arr = {'aliceblue': '#f0f8ff',
                 'antiquewhite': '#faebd7',
                 'aqua': '#00ffff',
                 'aquamarine': '#7fffd4',
                 'azure': '#f0ffff',
                 'beige': '#f5f5dc',
                 'bisque': '#ffe4c4',
                 'black': '#000000',
                 'blanchedalmond': '#ffebcd',
                 'blue': '#0000ff',
                 'blueviolet': '#8a2be2',
                 'brown': '#a52a2a',
                 'burlywood': '#deb887',
                 'cadetblue': '#5f9ea0',
                 'chartreuse': '#7fff00',
                 'chocolate': '#d2691e',
                 'coral': '#ff7f50',
                 'cornflowerblue': '#6495ed',
                 'cornsilk': '#fff8dc',
                 'crimson': '#dc143c',
                 'cyan': '#00ffff',
                 'darkblue': '#00008b',
                 'darkcyan': '#008b8b',
                 'darkgoldenrod': '#b8860b',
                 'darkgray': '#a9a9a9',
                 'darkgreen': '#006400',
                 'darkkhaki': '#bdb76b',
                 'darkmagenta': '#8b008b',
                 'darkolivegreen': '#556b2f',
                 'darkorange': '#ff8c00',
                 'darkorchid': '#9932cc',
                 'darkred': '#8b0000',
                 'darksalmon': '#e9967a',
                 'darkseagreen': '#8fbc8f',
                 'darkslateblue': '#483d8b',
                 'darkslategray': '#2f4f4f',
                 'darkturquoise': '#00ced1',
                 'darkviolet': '#9400d3',
                 'deeppink': '#ff1493',
                 'deepskyblue': '#00bfff',
                 'dimgray': '#696969',
                 'dodgerblue': '#1e90ff',
                 'firebrick': '#b22222',
                 'floralwhite': '#fffaf0',
                 'forestgreen': '#228b22',
                 'fuchsia': '#ff00ff',
                 'gainsboro': '#dcdcdc',
                 'ghostwhite': '#f8f8ff',
                 'gold': '#ffd700',
                 'goldenrod': '#daa520',
                 'gray': '#808080',
                 'green': '#008000',
                 'greenyellow': '#adff2f',
                 'honeydew': '#f0fff0',
                 'hotpink': '#ff69b4',
                 'indianred': '#cd5c5c',
                 'indigo': '#4b0082',
                 'ivory': '#fffff0',
                 'khaki': '#f0e68c',
                 'lavender': '#e6e6fa',
                 'lavenderblush': '#fff0f5',
                 'lawngreen': '#7cfc00',
                 'lemonchiffon': '#fffacd',
                 'lightblue': '#add8e6',
                 'lightcoral': '#f08080',
                 'lightcyan': '#e0ffff',
                 'lightgoldenrodyellow': '#fafad2', #seriously a color?
                 'lightgrey': '#d3d3d3',
                 'lightgreen': '#90ee90',
                 'lightpink': '#ffb6c1',
                 'lightsalmon': '#ffa07a',
                 'lightseagreen': '#20b2aa',
                 'lightskyblue': '#87cefa',
                 'lightslategray': '#778899',
                 'lightsteelblue': '#b0c4de',
                 'lightyellow': '#ffffe0',
                 'lime': '#00ff00',
                 'limegreen': '#32cd32',
                 'linen': '#faf0e6',
                 'magenta': '#ff00ff',
                 'maroon': '#800000',
                 'mediumaquamarine': '#66cdaa',
                 'mediumblue': '#0000cd',
                 'mediumorchid': '#ba55d3',
                 'mediumpurple': '#9370d8',
                 'mediumseagreen': '#3cb371',
                 'mediumslateblue': '#7b68ee',
                 'mediumspringgreen': '#00fa9a',
                 'mediumturquoise': '#48d1cc',
                 'mediumvioletred': '#c71585',
                 'midnightblue': '#191970',
                 'mintcream': '#f5fffa',
                 'mistyrose': '#ffe4e1',
                 'moccasin': '#ffe4b5',
                 'navajowhite': '#ffdead',
                 'navy': '#000080',
                 'oldlace': '#fdf5e6',
                 'olive': '#808000',
                 'olivedrab': '#6b8e23',
                 'orange': '#ffa500',
                 'orangered': '#ff4500',
                 'orchid': '#da70d6',
                 'palegoldenrod': '#eee8aa',
                 'palegreen': '#98fb98',
                 'paleturquoise': '#afeeee',
                 'palevioletred': '#d87093',
                 'papayawhip': '#ffefd5',
                 'peachpuff': '#ffdab9',
                 'peru': '#cd853f', 'pink': '#ffc0cb', 'plum': '#dda0dd', 'powderblue': '#b0e0e6',
                 'purple': '#800080', 'red': '#ff0000', 'rosybrown': '#bc8f8f', 'royalblue': '#4169e1',
                 'saddlebrown': '#8b4513', 'salmon': '#fa8072', 'sandybrown': '#f4a460', 'seagreen': '#2e8b57',
                 'seashell': '#fff5ee', 'sienna': '#a0522d', 'silver': '#c0c0c0', 'skyblue': '#87ceeb', 'slateblue': '#6a5acd',
                 'slategray': '#708090', 'snow': '#fffafa', 'springgreen': '#00ff7f', 'steelblue': '#4682b4', 'tan': '#d2b48c',
                 'teal': '#008080', 'thistle': '#d8bfd8', 'tomato': '#ff6347', 'turquoise': '#40e0d0', 'violet': '#ee82ee',
                 'wheat': '#f5deb3', 'white': '#ffffff', 'whitesmoke': '#f5f5f5', 'yellow': '#ffff00',
                 'yellowgreen': '#9acd32', 'yellowgreen': '#9acd32'};
    try:
        if(re.search('#[a-f|0-9]{6}', string)):
           return string;
        elif (re.search('#[a-f|0-9]{3}', string)):
           return '#'+(string[1]*2)+(string[2]*2)+(string[3]*2);
        return color_arr[string];
    except Exception, e:
        return '';
