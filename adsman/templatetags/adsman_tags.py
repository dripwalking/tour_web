# -*- coding: utf-8 -*-
from django import template
from countries.models import *
from avia.models import *
register = template.Library()

class AdsPostAttrNode(template.Node):
    def __init__(self, name, post):
        self.name = template.Variable(name)
        self.post = template.Variable(post)
    def render(self, context):
        res_name = self.name.resolve(context)
        res_post = self.post.resolve(context)
        for entry in res_post.entries.all():
            if entry.key == res_name:
                return entry.value
        return ""

class AdsHtmlSelectNode(template.Node):
    def __init__(self, name, values, captions, selected, suffix=None, style = "", multi = False):
        self.name = template.Variable(name)
        self.values = template.Variable(values)
        self.values_str = values
        self.captions = template.Variable(captions)
        self.captions_str = captions
        self.selected = template.Variable(selected)
        self.suffix = suffix
        self.style = style
        self.multi = multi
    def get_first(self, arr):
        if len(arr) > 0:
              return arr[0]
        return ""
        
    def tag_name(self):
        return "input"
    def type_attr(self):
        return ""
    def selected_attr(self):
        return "checked"
    def render_html(self, name, values, captions, selected):
        res = ""
        for i in range(len(values)):
            res += '<' + self.tag_name() + ' type="' + self.type_attr() + '" id="' +name + '" name="' + name + '" value="' + values[i] + '" '
            for sel_entry in selected:
                if values[i] != "" and values[i] == sel_entry:
                    res += ' ' + self.selected_attr() + ' '  
                    break           
            res += '/>' + captions[i] + '</' + self.tag_name() + '> '
        return res  
    
    def render(self, context):
        res_name = self.name.resolve(context)
        if self.suffix != None:
            res_name += "_" + self.suffix
        try:
            res_values = self.values.resolve(context)
        except:
            res_values = self.values_str   
        try:         
            res_captions = self.captions.resolve(context)
        except:
            res_captions = self.captions_str          
        try:
            res_selected = self.selected.resolve(context)[res_name]
        except:
            res_selected = ""
        values = res_values.split(',')
        captions = res_captions.split(',')
        selected = res_selected.split(',')
        return self.render_html(res_name, values, captions, selected)
    
class AdsSelectNode(AdsHtmlSelectNode):
     def render_html(self, name, values, captions, selected):
         res = u'<select id="' +name + '" name="' + name + '"'
         if self.multi:
             res += ' MULTIPLE SIZE="5" '
         res += u'> <option value="" >Выберите</option>'
         for i in range(len(values)):
            res += '<option value="' + values[i] + '" '
            if len(selected) == 1:
                #for sel_entry in selected[0]:
                #if values[i] == sel_entry:
                if values[i] == selected[0]:
                    res += ' selected '   
            res += ' >' + captions[i] + '</option>'       
         res += '</select> \n'
         return res
     
class AdsRadioGroupNode(AdsHtmlSelectNode):
    def type_attr(self):
        return "radio"
   

class AdsCheckBoxNode(AdsHtmlSelectNode):
    def type_attr(self):
        return "checkbox"       
    
class AdsTextBoxNode(AdsHtmlSelectNode):
      def render_html(self, name, values, captions, selected):
          #val = self.get_first(selected)
          val =",".join(selected)
          if val == "":
              val = ",".join(values)   
          if val == "_on":
              val = ""                   
          res = '<input name="' + name + '" type="text" value="' + val + '" class="' + self.style  +'" >'     
          return res
      
class AdsTextAreaNode(AdsHtmlSelectNode):
      def render_html(self, name, values, captions, selected):
          #val = self.get_first(selected)    
          val = ",".join(selected)            
          res = '<textarea id="' + name + '"  name="' + name + '" rows="6" cols="20" class="' + self.style  +  '" >' + val + '</textarea>'     
          return res
      
class AdsPhoneNode(template.Node):
      def __init__(self, name, values, captions, selected):
          self.text = AdsTextBoxNode(name, values, captions, selected)
          self.checkbox = AdsCheckBoxNode (name , values, captions, selected, "mc")
          
      def render(self, context):     
          return self.text.render(context) + self.checkbox.render(context)
      
class AdsValidNode (template.Node):
    def __init__(self, name, values):
        self.name = template.Variable(name)
        self.values = template.Variable(values)
        
    def render(self, context):
        res_name = self.name.resolve(context)
        res_values = self.values.resolve(context)
        try:
            val = res_values[res_name]
            return u'<font color="#FF0000">ошибка!</font>'
        except:
            return ""
      
class AdsRouteNode(template.Node):
    def __init__(self, name, selected):
        self.name = template.Variable(name)
        self.selected = template.Variable(selected)
        self.airports = [unicode(obj.title) for obj in  Airport.objects.order_by('title').all() ]
        self.fixed = [u"Москва", u"Санкт-Петербург", u"Екатеринбург", u"Калиниград", u"Сургут", u"Тюмень", u"Казань", u"Уфа", u"Самара", u"Нижний Новгород", u"Ростов-на-Дону", u"Новосибирск", u"Красноярск", u"Пермь", u"Краснодар", u"Минеральные Воды"]
        
    def _render_combo(self, name, titles, value):
        res = u'<select name="%s"> <option value="" >-------</option> ' % (name)
        selected = ""
        for title in titles:
            if title == value:
                selected = 'selected="selected" '
            else:
                selected = ""
            res += '<option value="%s" %s >%s</option>' % (title, selected, title)
        res += '</select>'
        return res
    
    
    def _get_value(self, values, key, default=""):
        try:
            return values[key]
        except:            
            return default
    
    def render(self, context):
        res_name = self.name.resolve(context)
        res_selected = self.selected.resolve(context)
        key1 = res_name + "_first"
        key2 = res_name + "_2"
        key3 = res_name + "_last"
        res = '<table><tr><td>'
        res += self._render_combo(key1, self.fixed, self._get_value(res_selected, key1, u"Москва")) + '</td> <td>-&gt;</td>'
        res += '<td>' + self._render_combo(key2, self.airports, self._get_value(res_selected, key2)) + '</td> <td>-&gt;</td>'
        res += '<td>' + self._render_combo(key3, self.fixed, self._get_value(res_selected, key3, u"Москва")) + '</td></tr></table>'
        return res
      
class AdsTravelStartNode(template.Node):
      def __init__(self, name, values, captions, selected):
          self.text = AdsTextBoxNode(name, values, captions, selected, "add")
          self.radio = AdsRadioGroupNode (name , values, captions, selected)
          
      def render(self, context):     
          return self.radio.render(context) +" <br> " + self.text.render(context)
  
class AdsSelectObjectNode(template.Node):
    def get_values(self):
        return []    
    def __init__(self, name, values, captions, selected, multi = False):
        data  = unicode(",".join( self.get_values() ) )
        self.select = AdsSelectNode(name, data, data, selected, None, "", multi)          
    def render(self, context):     
        return self.select.render(context)   
        
class AdsAircraftNode(AdsSelectObjectNode):
    def get_values(self):
        return [unicode(obj.title) for obj in  Aircraft.objects.order_by('title').all() ]
    
class AdsAirportNode(AdsSelectObjectNode):
    def get_values(self):
        return [unicode(obj.title) for obj in  Airport.objects.order_by('title').all() ]
    
class AdsAircompanyNode(AdsSelectObjectNode):
    def get_values(self):
        return [unicode(obj.title) for obj in  Aircompany.objects.order_by('title').all() ]
    
class AdsCountryNode(AdsSelectObjectNode):
    def get_values(self):
        return [unicode(obj.title) for obj in  Country.objects.order_by('title').all() ]

class AdsCruiseCompanyNode(AdsSelectObjectNode):
    def get_values(self):
        return [unicode(obj.title) for obj in  CruiseCompany.objects.order_by('title').all() ]

class AdsCruiseShipNode(AdsSelectObjectNode):
    def get_values(self):
        return [unicode(obj.title) for obj in  CruiseShip.objects.order_by('title').all() ]

def do_ads_travel_start(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsTravelStartNode(name, values, captions, selected)

def do_ads_country(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsCountryNode(name, values, captions, selected, True)

def do_ads_country_single(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsCountryNode(name, values, captions, selected)

def do_ads_cruise_company(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsCruiseCompanyNode(name, values, captions, selected)

def do_ads_cruise_ship(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsCruiseShipNode(name, values, captions, selected)

def do_ads_aircraft(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsAircraftNode(name, values, captions, selected)

def do_ads_airport(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsAirportNode(name, values, captions, selected)

def do_ads_aircompany(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsAircompanyNode(name, values, captions, selected)

def do_ads_route(parser, token):
    tag_name, name, selected = token.split_contents()
    return AdsRouteNode(name, selected)

def do_ads_select(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsSelectNode(name, values, captions, selected)

def do_ads_radio_group(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsRadioGroupNode(name, values, captions, selected)

def do_ads_checkbox(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsCheckBoxNode(name, values, captions, selected)

def do_ads_textbox(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsTextBoxNode(name, values, captions, selected)

def do_ads_textarea(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsTextAreaNode(name, values, captions, selected)

def do_ads_phone(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsPhoneNode(name, values, captions, selected)

def do_ads_valid(parser, token):
    tag_name, name, values = token.split_contents()
    return AdsValidNode(name, values)

def do_ads_calendar(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsTextBoxNode(name, values, captions, selected, None, "calendar")

def do_ads_pub_date(parser, token):
    tag_name, name, values, captions, selected = token.split_contents()
    return AdsTextAreaNode(name, values, captions, selected, None, "pub_date")

def do_ads_post_attr(parser, token):
    tag_name, name, post = token.split_contents()
    return AdsPostAttrNode(name, post)

do_ads_travel_start = register.tag("ads_travel_start", do_ads_travel_start)
do_ads_country = register.tag("ads_country", do_ads_country)
do_ads_country_single = register.tag("ads_country_single", do_ads_country_single)
do_ads_cruise_company = register.tag("ads_cruise_company", do_ads_cruise_company)
do_ads_cruise_ship = register.tag("ads_cruise_ship", do_ads_cruise_ship)
do_ads_aircraft = register.tag("ads_aircraft", do_ads_aircraft)
do_ads_airport = register.tag("ads_airport", do_ads_airport)
do_ads_aircompany = register.tag("ads_aircompany", do_ads_aircompany)
do_ads_route = register.tag("ads_route", do_ads_route)
do_ads_select = register.tag("ads_select", do_ads_select)
do_ads_radio_group = register.tag("ads_radio_group", do_ads_radio_group)
do_ads_checkbox = register.tag("ads_checkbox", do_ads_checkbox)
do_ads_textbox = register.tag("ads_textbox", do_ads_textbox)
do_ads_textarea = register.tag("ads_textarea", do_ads_textarea)
do_ads_phone = register.tag("ads_phone", do_ads_phone)
do_ads_valid = register.tag("ads_valid", do_ads_valid)
do_ads_calendar = register.tag("ads_calendar", do_ads_calendar)
do_ads_pub_date = register.tag("ads_pub_date", do_ads_pub_date)
do_ads_post_attr = register.tag("ads_post_attr", do_ads_post_attr)
