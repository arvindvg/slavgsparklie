import os
import webapp2
import cgi
from google.appengine.ext import ndb
from google.appengine.api import users
import jinja2
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from gaesessions import get_current_session
from gaesessions import set_current_session
import operator
import math
import urllib
import heapq
from google.appengine.api import channel
import uuid
import json
from collections import defaultdict
import braintree


jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'html')))  #editing the path location of the template files

class cluster_db(ndb.Model):
    Range = ndb.IntegerProperty(indexed=True)
    min_price = ndb.IntegerProperty(indexed=True)
    max_price = ndb.IntegerProperty(indexed=True)
    Size = ndb.StringProperty(indexed=True)
    Imperfections = ndb.StringProperty(indexed=True)
    Transparency = ndb.StringProperty(indexed=True)
    Sparkle = ndb.StringProperty(indexed=True)
    Cluster_no = ndb.IntegerProperty(indexed=True)
    Size_C = ndb.FloatProperty(indexed=True)
    Sparkle_C = ndb.FloatProperty(indexed=True)
    Transparency_C = ndb.FloatProperty(indexed=True)
    Imperfections_C = ndb.FloatProperty(indexed=True)
    Price_C = ndb.FloatProperty(indexed=True)
    Size_I = ndb.FloatProperty(indexed=True)
    Sparkle_I = ndb.FloatProperty(indexed=True)
    Transparency_I = ndb.FloatProperty(indexed=True)
    Imperfections_I = ndb.FloatProperty(indexed=True)
    Price_I = ndb.FloatProperty(indexed=True)
    Title = ndb.StringProperty(indexed=True)
    Tip = ndb.StringProperty(indexed=True)

class sample_inventory_v2(ndb.Model):
    Price = ndb.FloatProperty(indexed=True)
    count = ndb.IntegerProperty(indexed=True)
    Size = ndb.FloatProperty(indexed=True)
    Imperfections = ndb.FloatProperty(indexed=True)
    Transparency = ndb.FloatProperty(indexed=True)
    Sparkle = ndb.FloatProperty(indexed=True)
    Imperfections_real = ndb.StringProperty(indexed=True)
    Transparency_real = ndb.StringProperty(indexed=True)
    Sparkle_real = ndb.StringProperty(indexed=True)
    Merchant = ndb.StringProperty(indexed=True)
    RingName = ndb.StringProperty(indexed=True)
    Ring_des = ndb.StringProperty(indexed=True)
    Shape = ndb.StringProperty(indexed=True)
    Setting = ndb.StringProperty(indexed=True)
    Metal = ndb.StringProperty(indexed=True)
    Metal_quality = ndb.StringProperty(indexed=True)
    RingName_raw = ndb.StringProperty(indexed=True)
    Merchant_id = ndb.IntegerProperty(indexed=True)
    prod_url1 = ndb.StringProperty(indexed=True)
    image_url1 = ndb.StringProperty(indexed=True)
    prod_url2 = ndb.StringProperty(indexed=True)
    prod_url3 = ndb.StringProperty(indexed=True)
    image_url2 = ndb.StringProperty(indexed=True)

class user_input_db(ndb.Model):
    #sessionID = ndb.StringProperty(indexed=True)
    price_lower = ndb.IntegerProperty(indexed=True)
    price_upper = ndb.IntegerProperty(indexed=True)
    shape = ndb.StringProperty(indexed=True)
    setting = ndb.StringProperty(indexed=True)
    ring_metal = ndb.StringProperty(indexed=True)
    cluster_title = ndb.StringProperty(indexed=True) 
    ring_selection = ndb.IntegerProperty(indexed=True) 
    date = ndb.DateTimeProperty(auto_now_add=True)

class email2_db(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    gen_feedback = ndb.StringProperty(indexed=True)
    recomm_feedback = ndb.StringProperty(indexed=True)
    comp_feedback= ndb.StringProperty(indexed=True)
    dtype_feedback = ndb.StringProperty(indexed=True)
    question_feedback = ndb.StringProperty(indexed=True)
    sex = ndb.StringProperty(indexed=True)
    married = ndb.StringProperty(indexed=True)
    ring = ndb.StringProperty(indexed=True)
    online = ndb.StringProperty(indexed=True)
    shop_style = ndb.StringProperty(indexed=True)

class Step1(webapp2.RequestHandler):

    def get(self):
        session = get_current_session()
        c = session.get('count', 0) # I dont' fully understand why a get() function needs to be initalized if no cookie available
        session['count'] = c + 1
        template = jinja_environment.get_template('step1.html')
        self.response.out.write(template.render())
        #self.redirect('html/step1.html')

class Step2(webapp2.RequestHandler):

    def get(self):
        session = get_current_session()
        count = session.get('count')
        internalcounter = session.get('internalCounter', 0)
        template_values = {}
        template_values['count'] = count
        template_values['internalCounter'] = internalcounter
        template = jinja_environment.get_template('step2.html')
        self.response.out.write(template.render(template_values))
        #self.redirect('html/step2.html')

    def post(self):
        session = get_current_session()
        internalCounter = self.request.get('internalCounter')
        user_shape = self.request.get('shape')
        session['user_shape'] = user_shape
        session['internalCounter'] = internalCounter

class Step3(webapp2.RequestHandler):

    def get(self):
        template = jinja_environment.get_template('step3.html')
        self.response.out.write(template.render())
        #self.redirect('html/step2.html')

    def post(self):
        session = get_current_session()
        user_setting = self.request.get('setting')
        next = self.request.get('next')
        back = self.request.get('back')
        session['user_setting'] = user_setting
        if back =="back":
            self.redirect('/step2')
        elif next == "next":
            if user_setting != "":
                self.redirect('/step4')
            else: 
                self.redirect('/step3')

class Step4(webapp2.RequestHandler):

    def get(self):
        template = jinja_environment.get_template('step4.html')
        self.response.out.write(template.render())
        #self.redirect('html/step2.html')

    def post(self):
        session = get_current_session()
        user_ring = self.request.get('ring')
        next = self.request.get('next')
        back = self.request.get('back')
        session['user_ring'] = user_ring
        if back =="back":
            self.redirect('/step3')
        elif next == "next":
            if user_ring != "":
                self.redirect('/step5')
            else: 
                self.redirect('/step4')

class Step5(webapp2.RequestHandler):

    def get(self):
        template = jinja_environment.get_template('step5.html')
        self.response.out.write(template.render())
        #self.redirect('html/step2.html')

    def post(self):
        session = get_current_session()
        user_price = self.request.get('price')
        user_price_lower,user_price_upper = user_price.split(",") 
        user_price_lower = int(user_price_lower)
        user_price_upper = int(user_price_upper)
        user_ring = session.get('user_ring')
        user_setting = session.get('user_setting')
        user_shape = session.get('user_shape')

        range = user_price_upper - user_price_lower 
        next = self.request.get('next')
        back = self.request.get('back')
        session['user_price_lower'] = user_price_lower
        session['user_price_upper'] = user_price_upper
        session['range'] = range
        if back =="back":
            self.redirect('/step4')
        elif next == "next":
            if user_price_lower != "" and user_price_upper != "" and range <= 2500:
                self.redirect('/step6')
            else: 
                self.redirect('/step5')

class Step6(webapp2.RequestHandler):

    def get(self):
        clus_size_list = []
        clus_price_list = []
        clus_imperfection_list = []
        clus_sparkle_list = []
        clus_transperency_list = []
        clus_title = []
        clus_tip = []
        clus_price_raw = []
        template_values = {}
        session = get_current_session()
        user_ring = session.get('user_ring')
        user_price_lower = session.get('user_price_lower')
        user_price_upper = session.get('user_price_upper')
        user_setting = session.get('user_setting')
        user_shape = session.get('user_shape')
        range = session.get('range')
        channel_id = "1"
        channel_token = channel.create_channel(channel_id)
        template_values['token'] = channel_token
        session['token'] = channel_token
        clus_query = cluster_db.query(cluster_db.Range == int(range),cluster_db.min_price == int(user_price_lower),cluster_db.max_price == int(user_price_upper)).fetch()	
        for result in clus_query:
            clus_size_list.append(result.Size)
            clus_imperfection_list.append(result.Imperfections)
            clus_sparkle_list.append(result.Sparkle)
            clus_transperency_list.append(result.Transparency)
            clus_title.append(result.Title)
            clus_tip.append(result.Tip)
            clus_price_raw.append(result.Price_C)

        max_size=max(clus_size_list)
        max_imperfection=max(clus_imperfection_list)
        max_sparkle=max(clus_sparkle_list)
        max_transparency=max(clus_transperency_list)
        max_color="#D1D1D1"
        min_color=""
        j = 0
        for i in xrange(0,4):
            j = j +1
            template_values['size%d' %j] = clus_size_list[i]
            template_values['price%d' %j] = "{:,}".format(int(math.ceil(clus_price_raw[i]/100.0)) * 100 )
            template_values['price_range%d' %j] = int((float(int(clus_price_raw[i]) - int(user_price_lower)) / (int(user_price_upper) - int(user_price_lower)))*100) 
            template_values['purity%d' %j] = clus_imperfection_list[i]
            template_values['sparkle%d' %j] = clus_sparkle_list[i]
            template_values['transparency%d' %j] = clus_transperency_list[i]
            template_values['tip%d' %j] = clus_tip[i]
            template_values['title%d' %j] = clus_title[i]
            if clus_size_list[i] == max_size :
                template_values['color_size%d' %j] = max_color
            else :
                template_values['color_size%d' %j] = min_color
            if clus_imperfection_list[i] == max_imperfection :
                template_values['color_purity%d' %j] = max_color
            else :
                template_values['color_purity%d' %j] = min_color
            if clus_sparkle_list[i] == max_sparkle :
                template_values['color_sparkle%d' %j] = max_color
            else :
                template_values['color_sparkle%d' %j] = min_color
            if clus_transperency_list[i] == max_transparency :
                template_values['color_transparency%d' %j] = max_color
            else :
                template_values['color_transparency%d' %j] = min_color
        template_values['user_price_lower'] = "{:,}".format(int(user_price_lower))
        template_values['user_price_upper'] = "{:,}".format(int(user_price_upper))	
        session['clus_query'] = clus_query
        self.response.out.write(json.dumps(template_values))


    def post(self):
        session = get_current_session()
        channel_id=session.get('token')
        channel.send_message(channel_id,"5%")
        user_shape_list = []
        user_setting_list = []
        user_ring_list = []
        user_price_lower = session.get('user_price_lower')
        user_price_lower = float(user_price_lower)	
        user_price_upper = session.get('user_price_upper')
        user_price_upper = float(user_price_upper)	
        user_setting = session.get('user_setting')
        user_setting = user_setting.upper()
        user_setting_list.append(user_setting)
        user_shape = session.get('user_shape')
        user_shape = user_shape.upper()
        user_shape_list.append(user_shape)
        user_ring = session.get('user_ring')
        user_ring = user_ring.upper()
        user_ring_list.append(user_ring)
        range = session.get('range')
        clus_query = session.get('clus_query')
        user_selection = self.request.get('select')
        session['user_selection'] = user_selection
        user_selection = int(user_selection)
        cluster_size = []
        cluster_Sparkle = []
        cluster_Transparency = []
        cluster_Imperfections = []
        cluster_price = []
        cluster_size_influence = []
        cluster_sparkle_influence = []
        cluster_trans_influence = []
        cluster_imperfection_influence = []
        cluster_price_influence = []
        cluster_title = []

        inventory_size={}
        inventory_Sparkle = {}
        inventory_Transparency = {}
        inventory_Imperfections = {}
        inventory_price_actual = {}
        inventory_merchant = {}
        inventory_shape = {}
        inventory_setting = {}
        inventory_metal = {}
        product_url = {}
        image_url = {}
            
        pred_carat = {}
        pred_Sparkle = {}
        pred_Transparency = {}
        pred_Imperfections = {}
        pred_carat_b = {}
        pred_price = {}
        price_diff_model = {}
        price_diff_cluster = {}
        size_diff = {}
        sparkle_diff = {}
        transparency_diff = {}
        imperfections_diff = {}
        pred_price_score = {}
        clus_price_score = {}
        clus_size_score = {}
        clus_sparkle_score = {}
        clus_transparency_score = {}
        clus_imperfections_score = {}
        composite_score= {}
        composite_score_raw = {}

        best_overall_score_0 = {}
        best_overall_score_1 = {}
        best_overall_score_2 = {}
        best_overall_score_3 = {}
        best_overall_score_4 = {}

        best_imperfections_score_0 = {}
        best_imperfections_score_1 = {}
        best_imperfections_score_2 = {}
        best_imperfections_score_3 = {}
        best_imperfections_score_4 = {}

        best_transparency_score_0 = {}
        best_transparency_score_1 = {}
        best_transparency_score_2 = {}
        best_transparency_score_3 = {}
        best_transparency_score_4 = {}

        best_sparkle_score_0 = {}
        best_sparkle_score_1 = {}
        best_sparkle_score_2 = {}
        best_sparkle_score_3 = {}
        best_sparkle_score_4 = {}

        best_size_score_0 = {}
        best_size_score_1 = {}
        best_size_score_2 = {}
        best_size_score_3 = {}
        best_size_score_4 = {}
        
        best_overall_price = {}
        best_imperfections_price = {}
        best_transparency_price = {}
        best_sparkle_price = {}
        best_size_price = {}

        best_overall_merchant = {}
        best_imperfections_merchant = {}
        best_transparency_merchant = {}
        best_sparkle_merchant = {}
        best_size_merchant = {}

        best_overall_product_url = {}
        best_imperfections_product_url = {}
        best_transparency_product_url = {}
        best_sparkle_product_url = {}
        best_size_product_url = {}

        best_overall_image_url = {}
        best_imperfections_image_url = {}
        best_transparency_image_url = {}
        best_sparkle_image_url = {}
        best_size_image_url = {}

        #inventory_size2 = []
        #above this are all initalization of list and dictionaries
        #below this is to calculate information for population on step 3 page

        #inventory_query = sample_inventory_v2.query(sample_inventory_v2.Price >= user_price_lower,sample_inventory_v2.Price <= user_price_upper,sample_inventory_v2.Shape == user_shape,sample_inventory_v2.Setting == user_setting,sample_inventory_v2.Metal == user_ring).fetch()
        inventory_query = sample_inventory_v2.query(sample_inventory_v2.Price >= user_price_lower,sample_inventory_v2.Price <= user_price_upper).fetch()
        #inventory_query1 = sample_inventory_v2.query(sample_inventory_v2.Shape == user_shape).fetch(),sample_inventory_v2.Setting == "PRONG",sample_inventory_v2.Metal == "GOLD"
        #inventory_query2= sample_inventory_v2.query(sample_inventory_v2.Setting == user_setting).fetch()
        #inventory_query3 = sample_inventory_v2.query(sample_inventory_v2.Metal == user_ring).fetch()
        for result in clus_query:
            if result.Cluster_no == user_selection:
                cluster_size.append(result.Size_C)
                cluster_Sparkle.append(result.Sparkle_C)
                cluster_Transparency.append(result.Transparency_C)
                cluster_Imperfections.append(result.Imperfections_C)
                cluster_price.append(result.Price_C)
                cluster_size_influence.append(result.Size_I)
                cluster_sparkle_influence.append(result.Sparkle_I)
                cluster_trans_influence.append(result.Transparency_I)
                cluster_imperfection_influence.append(result.Imperfections_I)
                cluster_price_influence.append(result.Price_I)
                cluster_title.append(result.Title)
        for result in inventory_query:
                inventory_size[result.count] = result.Size
                inventory_Sparkle[result.count] = result.Sparkle
                inventory_Transparency[result.count] = result.Transparency
                inventory_Imperfections[result.count] = result.Imperfections
                inventory_price_actual[result.count] = result.Price
                inventory_shape[result.count] = result.Shape
                inventory_setting[result.count] = result.Setting
                inventory_metal[result.count] = result.Metal
                product_url[result.count] = result.prod_url1
                image_url[result.count] = result.image_url1			
            # Prediction and optimization variable creation
        channel.send_message(channel_id,"25%")
        for key in inventory_price_actual:
            #Parameter estimates implementation
            pred_carat[key] = (5.77287 + (1.11253*inventory_size[key]))
            if inventory_Sparkle[key] == 2:
                pred_Sparkle[key] = -0.01036
            elif inventory_Sparkle[key] == 3:
                pred_Sparkle[key] = -0.034560
            elif inventory_Sparkle[key] == 4:
                pred_Sparkle[key] = -0.01272
            elif inventory_Sparkle[key] == 5:
                pred_Sparkle[key] = 0.16027
            else :
                pred_Sparkle[key] =0
            if inventory_Transparency[key] == 2:
                pred_Transparency[key] = 0.16078
            elif inventory_Transparency[key] == 3:
                pred_Transparency[key] = 0.29146
            elif inventory_Transparency[key] == 4:
                pred_Transparency[key] = 0.37335
            elif inventory_Transparency[key] == 5:
                pred_Transparency[key] = 0.44596
            elif inventory_Transparency[key] == 6:
                pred_Transparency[key] = 0.45475
            elif inventory_Transparency[key] == 7:
                pred_Transparency[key] = 0.55459
            else:
                pred_Transparency[key] = 0
            if inventory_Imperfections[key] == 2:
                pred_Imperfections[key] = 0.15460
            elif inventory_Imperfections[key] == 3:
                pred_Imperfections[key] = 0.29614
            elif inventory_Imperfections[key] == 4:
                pred_Imperfections[key] = 0.44228
            elif inventory_Imperfections[key] == 5:
                pred_Imperfections[key] = 0.51656 
            elif inventory_Imperfections[key] == 6:
                pred_Imperfections[key] = .57903
            elif inventory_Imperfections[key] == 7:
                pred_Imperfections[key] = 0.66721
            elif inventory_Imperfections[key] == 8:
                pred_Imperfections[key] = 1.03907
            else:
                pred_Imperfections[key] = 0
            if inventory_size[key] > 0.59 and inventory_size[key] <= 1:
                pred_carat_b[key] = 0.98669
            elif inventory_size[key] >1 and inventory_size[key] <= 1.5:
                pred_carat_b[key] = 1.47039
            elif inventory_size[key] >1.5 and inventory_size[key] <= 2:
                pred_carat_b[key] = 1.54416
            elif inventory_size[key] >2 :
                pred_carat_b[key] = 1.30258
            else:
                pred_carat_b[key] = 0
            pred_price[key] = ((math.exp(pred_carat[key] + pred_Sparkle[key] + pred_Imperfections[key] + pred_Transparency[key] + pred_carat_b[key])) * (math.exp((0.3536244*0.3536244)/2)))
            # Calculate differences between actual inventory characteristics and predicted price/cluster characteristics
            price_diff_model[key] = ((inventory_price_actual[key] - pred_price[key])/inventory_price_actual[key]) * 100
            price_diff_cluster[key] = ((inventory_price_actual[key] - cluster_price[0]) / inventory_price_actual[key])* 100
            size_diff[key] = ((inventory_size[key] - cluster_size[0]) / inventory_size[key] )  * 100
            sparkle_diff[key] = ((inventory_Sparkle[key] - cluster_Sparkle[0]) / inventory_Sparkle[key] ) * 100
            transparency_diff[key] = ((inventory_Transparency[key] - cluster_Transparency[0]) / inventory_Transparency[key] ) * 100
            imperfections_diff[key] = ((inventory_Imperfections[key] - cluster_Imperfections[0]) / inventory_Imperfections[key] ) * 100
        channel.send_message(channel_id,"50%")
        #Scoring System Implementation
        for key in price_diff_model:
        # Predicted Price Score
            if price_diff_model[key] > -5 and  price_diff_model[key] <= 0:
                pred_price_score[key] = 0
            elif price_diff_model[key] > -10 and  price_diff_model[key] <=  -5:
                pred_price_score[key] = 1
            elif price_diff_model[key] > -15 and  price_diff_model[key] <=  -10:
                pred_price_score[key] = 2
            elif price_diff_model[key] > -20 and  price_diff_model[key] <=  -15:
                pred_price_score[key] = 3
            elif price_diff_model[key] < -20:
                pred_price_score[key] = 4
            elif price_diff_model[key] > 0 and  price_diff_model[key] <=  5:
                pred_price_score[key] = 0
            elif price_diff_model[key] > 5 and  price_diff_model[key] <=  10:
                pred_price_score[key] = -1
            elif price_diff_model[key] > 10 and  price_diff_model[key] <=  15:
                pred_price_score[key] = -2
            elif price_diff_model[key] > 15 and  price_diff_model[key] <=  20:
                pred_price_score[key] = -3
            elif price_diff_model[key] > 20 :
                pred_price_score[key] = -4
        # Cluster Price Score - Is not going to have much influence for now - Clusters already have price range restrictions
            if price_diff_cluster[key] > -5 and  price_diff_cluster[key] <= 0:
                clus_price_score[key] = 0
            elif price_diff_cluster[key] > -10 and  price_diff_cluster[key] <=  -5:
                clus_price_score[key] = 1
            elif price_diff_cluster[key] > -15 and  price_diff_cluster[key] <=  -10:
                clus_price_score[key] = 2
            elif price_diff_cluster[key] > -20 and  price_diff_cluster[key] <=  -15:
                clus_price_score[key] = 3
            elif price_diff_cluster[key] < -20:
                clus_price_score[key] = 4
            elif price_diff_cluster[key] > 0 and  price_diff_cluster[key] <=  5:
                clus_price_score[key] = 0
            elif price_diff_cluster[key] > 5 and  price_diff_cluster[key] <=  10:
                clus_price_score[key] = -1
            elif price_diff_cluster[key] > 10 and  price_diff_cluster[key] <=  15:
                clus_price_score[key] = -2
            elif price_diff_cluster[key] > 15 and  price_diff_cluster[key] <=  20:
                clus_price_score[key] = -3
            elif price_diff_cluster[key] > 20 :
                clus_price_score[key] = -4
        # Cluster Size Score
            if size_diff[key] > -5 and  size_diff[key] <= 0:
                clus_size_score[key] = 0
            elif size_diff[key] > -10 and  size_diff[key] <=  -5:
                clus_size_score[key] = -1
            elif size_diff[key] > -15 and  size_diff[key] <=  -10:
                clus_size_score[key] = -2
            elif size_diff[key] > -20 and  size_diff[key] <=  -15:
                clus_size_score[key] = -3
            elif size_diff[key] < -20:
                clus_size_score[key] = -4
            elif size_diff[key] > 0 and  size_diff[key] <=  5:
                clus_size_score[key] = 0
            elif size_diff[key] > 5 and  size_diff[key] <=  10:
                clus_size_score[key] = 1
            elif size_diff[key] > 10 and  size_diff[key] <=  15:
                clus_size_score[key] = 2
            elif size_diff[key] > 15 and  size_diff[key] <=  20:
                clus_size_score[key] = 3
            elif size_diff[key] > 20 :
                clus_size_score[key] = 4
        # Sparkle Score
            if sparkle_diff[key] > -5 and  sparkle_diff[key] <= 0:
                clus_sparkle_score[key] = 0
            elif sparkle_diff[key] > -10 and  sparkle_diff[key] <=  -5:
                clus_sparkle_score[key] = -1
            elif sparkle_diff[key] > -15 and  sparkle_diff[key] <=  -10:
                clus_sparkle_score[key] = -2
            elif sparkle_diff[key] > -20 and  sparkle_diff[key] <=  -15:
                clus_sparkle_score[key] = -3
            elif sparkle_diff[key] < -20:
                clus_sparkle_score[key] = -4
            elif sparkle_diff[key] > 0 and  sparkle_diff[key] <=  5:
                clus_sparkle_score[key] = 0
            elif sparkle_diff[key] > 5 and  sparkle_diff[key] <=  10:
                clus_sparkle_score[key] = 1
            elif sparkle_diff[key] > 10 and  sparkle_diff[key] <=  15:
                clus_sparkle_score[key] = 2
            elif sparkle_diff[key] > 15 and  sparkle_diff[key] <=  20:
                clus_sparkle_score[key] = 3
            elif sparkle_diff[key] > 20 :
                clus_sparkle_score[key] = 4
        # Transparency Score
            if transparency_diff[key] > -5 and  transparency_diff[key] <= 0:
                clus_transparency_score[key] = 0
            elif transparency_diff[key] > -10 and  transparency_diff[key] <=  -5:
                clus_transparency_score[key] = -1
            elif transparency_diff[key] > -15 and  transparency_diff[key] <=  -10:
                clus_transparency_score[key] = -2
            elif transparency_diff[key] > -20 and  transparency_diff[key] <=  -15:
                clus_transparency_score[key] = -3
            elif transparency_diff[key] < -20:
                clus_transparency_score[key] = -4
            elif transparency_diff[key] > 0 and  transparency_diff[key] <=  5:
                clus_transparency_score[key] = 0
            elif transparency_diff[key] > 5 and  transparency_diff[key] <=  10:
                clus_transparency_score[key] = 1
            elif transparency_diff[key] > 10 and  transparency_diff[key] <=  15:
                clus_transparency_score[key] = 2
            elif transparency_diff[key] > 15 and  transparency_diff[key] <=  20:
                clus_transparency_score[key] = 3
            elif transparency_diff[key] > 20 :
                clus_transparency_score[key] = 4
        # Imperfections Score
            if imperfections_diff[key] > -5 and  imperfections_diff[key] <= 0:
                clus_imperfections_score[key] = 0
            elif imperfections_diff[key] > -10 and  imperfections_diff[key] <=  -5:
                clus_imperfections_score[key] = -1
            elif imperfections_diff[key] > -15 and  imperfections_diff[key] <=  -10:
                clus_imperfections_score[key] = -2
            elif imperfections_diff[key] > -20 and  imperfections_diff[key] <=  -15:
                clus_imperfections_score[key] = -3
            elif imperfections_diff[key] < -20:
                clus_imperfections_score[key] = -4
            elif imperfections_diff[key] > 0 and  imperfections_diff[key] <=  5:
                clus_imperfections_score[key] = 0
            elif imperfections_diff[key] > 5 and  imperfections_diff[key] <=  10:
                clus_imperfections_score[key] = 1
            elif imperfections_diff[key] > 10 and  imperfections_diff[key] <=  15:
                clus_imperfections_score[key] = 2
            elif imperfections_diff[key] > 15 and  imperfections_diff[key] <=  20:
                clus_imperfections_score[key] = 3
            elif imperfections_diff[key] > 20 :
                clus_imperfections_score[key] = 4
            composite_score[key] = cluster_price_influence[0]*pred_price_score[key] + cluster_price_influence[0]*clus_price_score[key] + cluster_imperfection_influence[0]*clus_imperfections_score[key] + cluster_trans_influence[0]*clus_transparency_score[key] + cluster_sparkle_influence[0]*clus_sparkle_score[key] + cluster_size_influence[0]*clus_size_score[key]
            composite_score_raw[key] = pred_price_score[key] + clus_price_score[key] + clus_imperfections_score[key] + clus_transparency_score[key] + clus_sparkle_score[key] + clus_size_score[key]
        channel.send_message(channel_id,"75%")		
        for k,v in inventory_shape.items():
            if v not in user_shape_list[0]:
                del inventory_shape[k]
 
        shape_list = inventory_shape.keys()

        for k,v in inventory_setting.items():
            if v not in user_setting_list[0]:
                del inventory_setting[k]
 
        setting_list = inventory_setting.keys()

        for k,v in inventory_metal.items():
            if v not in user_ring_list[0]:
                del inventory_metal[k]
 
        metal_list = inventory_metal.keys()
        
        for k, v in composite_score.items():
            if k not in shape_list:
                del composite_score[k]

        for k, v in composite_score.items():
            if k not in setting_list:
                del composite_score[k]

        for k, v in composite_score.items():
            if k not in metal_list:
                del composite_score[k]
        # Keep only those that score a minimum of 0 i.e. average
                
        for k, v in composite_score.items():
            if v > 500:
                del composite_score[k]

        key_select_list = composite_score.keys()

        # Delete those which don't meet the minimum criteria
        for k, v in inventory_Imperfections.items():
            if k not in key_select_list:
                del inventory_Imperfections[k]

        for k, v in inventory_Transparency.items():
            if k not in key_select_list:
                del inventory_Transparency[k]

        for k, v in inventory_Sparkle.items():
            if k not in key_select_list:
                del inventory_Sparkle[k]

        for k, v in inventory_size.items():
            if k not in key_select_list:
                del inventory_size[k]

        #Sort dictionary and keep top n - Change here is more options are needed - Preserves descending order in the output dictionary
        n = 5
        best_overall = heapq.nlargest(n,composite_score.items(), key=operator.itemgetter(1))
        best_overall = map(operator.itemgetter(0),best_overall)
        best_imperfections = heapq.nlargest(n,inventory_Imperfections.items(), key=operator.itemgetter(1))
        best_imperfections = map(operator.itemgetter(0),best_imperfections)
        best_transparency = heapq.nlargest(n,inventory_Transparency.items(), key=operator.itemgetter(1))
        best_transparency = map(operator.itemgetter(0),best_transparency)
        best_sparkle = heapq.nlargest(n,inventory_Sparkle.items(), key=operator.itemgetter(1))
        best_sparkle = map(operator.itemgetter(0),best_sparkle)
        best_size = heapq.nlargest(n,inventory_size.items(), key=operator.itemgetter(1))
        best_size = map(operator.itemgetter(0),best_size)
        channel.send_message(channel_id,"90%")		
        # Collect Composite Score - 0
        for k, v in composite_score_raw.items():
            if k in best_overall:
                best_overall_score_0[k] = composite_score_raw[k]//float(6)
            if k in best_imperfections:
                best_imperfections_score_0[k] = composite_score_raw[k]//float(6)
            if k in best_transparency:
                best_transparency_score_0[k] = composite_score_raw[k]//float(6)
            if k in best_sparkle:
                best_sparkle_score_0[k] = composite_score_raw[k]//float(6)
            if k in best_size:
                best_size_score_0[k] = composite_score_raw[k]//float(6)

        # Collect Imperfection Score - 1
        for k, v in clus_imperfections_score.items():
            if k in best_overall:
                best_overall_score_1[k] = clus_imperfections_score[k]//float(1)
            if k in best_imperfections:
                best_imperfections_score_1[k] = clus_imperfections_score[k]//float(1)
            if k in best_transparency:
                best_transparency_score_1[k] = clus_imperfections_score[k]//float(1)
            if k in best_sparkle:
                best_sparkle_score_1[k] = clus_imperfections_score[k]//float(1)
            if k in best_size:
                best_size_score_1[k] = clus_imperfections_score[k]//float(1)

        # Collect Transparency Score - 2
        for k, v in clus_transparency_score.items():
            if k in best_overall:
                best_overall_score_2[k] = clus_transparency_score[k]//float(1)
            if k in best_imperfections:
                best_imperfections_score_2[k] = clus_transparency_score[k]//float(1)
            if k in best_transparency:
                best_transparency_score_2[k] = clus_transparency_score[k]//float(1)
            if k in best_sparkle:
                best_sparkle_score_2[k] = clus_transparency_score[k]//float(1)
            if k in best_size:
                best_size_score_2[k] = clus_transparency_score[k]//float(1)
                
        # Collect Sparkle Score - 3
        for k, v in clus_sparkle_score.items():
            if k in best_overall:
                best_overall_score_3[k] = clus_sparkle_score[k]//float(1)
            if k in best_imperfections:
                best_imperfections_score_3[k] = clus_sparkle_score[k]//float(1)
            if k in best_transparency:
                best_transparency_score_3[k] = clus_sparkle_score[k]//float(1)
            if k in best_sparkle:
                best_sparkle_score_3[k] = clus_sparkle_score[k]//float(1)
            if k in best_size:
                best_size_score_3[k] = clus_sparkle_score[k]//float(1)

        # Collect Size Score - 4
        for k, v in clus_size_score.items():
            if k in best_overall:
                best_overall_score_4[k] = clus_size_score[k]//float(1)
            if k in best_imperfections:
                best_imperfections_score_4[k] = clus_size_score[k]//float(1)
            if k in best_transparency:
                best_transparency_score_4[k] = clus_size_score[k]//float(1)
            if k in best_sparkle:
                best_sparkle_score_4[k] = clus_size_score[k]//float(1)
            if k in best_size:
                best_size_score_4[k] = clus_size_score[k]//float(1)

        # Collect Price			
        for k, v in inventory_price_actual.items():
            if k in best_overall:
                best_overall_price[k] = inventory_price_actual[k]
            if k in best_imperfections:
                best_imperfections_price[k] = inventory_price_actual[k]
            if k in best_transparency:
                best_transparency_price[k] = inventory_price_actual[k]
            if k in best_sparkle:
                best_sparkle_price[k] = inventory_price_actual[k]
            if k in best_size:
                best_size_price[k] = inventory_price_actual[k]
                
        # Collect Merchant Name			
        for k, v in inventory_merchant.items():
            if k in best_overall:
                best_overall_merchant[k] = inventory_merchant[k]
            if k in best_imperfections:
                best_imperfections_merchant[k] = inventory_merchant[k]
            if k in best_transparency:
                best_transparency_merchant[k] = inventory_merchant[k]
            if k in best_sparkle:
                best_sparkle_merchant[k] = inventory_merchant[k]
            if k in best_size:
                best_size_merchant[k] = inventory_merchant[k]

        # Collect Product URL			
        for k, v in product_url.items():
            if k in best_overall:
                best_overall_product_url[k] = product_url[k]
            if k in best_imperfections:
                best_imperfections_product_url[k] = product_url[k]
            if k in best_transparency:
                best_transparency_product_url[k] = product_url[k]
            if k in best_sparkle:
                best_sparkle_product_url[k] = product_url[k]
            if k in best_size:
                best_size_product_url[k] = product_url[k]

        # Collect Image URL			
        for k, v in image_url.items():
            if k in best_overall:
                best_overall_image_url[k] = image_url[k]
            if k in best_imperfections:
                best_imperfections_image_url[k] = image_url[k]
            if k in best_transparency:
                best_transparency_image_url[k] = image_url[k]
            if k in best_sparkle:
                best_sparkle_image_url[k] = image_url[k]
            if k in best_size:
                best_size_image_url[k] = image_url[k]

        for i in xrange(0,5):

            for key in locals()["best_overall_score_"+str(i)]:				
                if locals()["best_overall_score_"+str(i)][key] < -3 :
                    locals()["best_overall_score_"+str(i)][key] = locals()["best_overall_score_"+str(i)][key] + 4.5
                elif locals()["best_overall_score_"+str(i)][key] >= -3 and  locals()["best_overall_score_"+str(i)][key] < -2:
                    locals()["best_overall_score_"+str(i)][key] = locals()["best_overall_score_"+str(i)][key] + 4
                elif locals()["best_overall_score_"+str(i)][key] >= -2 and  locals()["best_overall_score_"+str(i)][key] < -1:
                    locals()["best_overall_score_"+str(i)][key] = locals()["best_overall_score_"+str(i)][key] + 3.5
                elif locals()["best_overall_score_"+str(i)][key] >= -1 and  locals()["best_overall_score_"+str(i)][key] < 0:
                    locals()["best_overall_score_"+str(i)][key] = locals()["best_overall_score_"+str(i)][key] + 3
                elif locals()["best_overall_score_"+str(i)][key] >= 0 and  locals()["best_overall_score_"+str(i)][key] < 1:
                    locals()["best_overall_score_"+str(i)][key] = locals()["best_overall_score_"+str(i)][key] + 3
                elif locals()["best_overall_score_"+str(i)][key] >= 1 and  locals()["best_overall_score_"+str(i)][key] < 2:
                    locals()["best_overall_score_"+str(i)][key] = locals()["best_overall_score_"+str(i)][key] + 2.5
                elif locals()["best_overall_score_"+str(i)][key] >= 2 and  locals()["best_overall_score_"+str(i)][key] < 3:
                    locals()["best_overall_score_"+str(i)][key] = locals()["best_overall_score_"+str(i)][key] + 2
                elif locals()["best_overall_score_"+str(i)][key] >= 3 and  locals()["best_overall_score_"+str(i)][key] < 4:
                    locals()["best_overall_score_"+str(i)][key] = locals()["best_overall_score_"+str(i)][key] + 1.5
                elif locals()["best_overall_score_"+str(i)][key] >= 4 :
                    locals()["best_overall_score_"+str(i)][key] = locals()["best_overall_score_"+str(i)][key] + 1

            for key in locals()["best_imperfections_score_"+str(i)]:				
                if locals()["best_imperfections_score_"+str(i)][key] < -3 :
                    locals()["best_imperfections_score_"+str(i)][key] = locals()["best_imperfections_score_"+str(i)][key] + 4.5
                elif locals()["best_imperfections_score_"+str(i)][key] >= -3 and  locals()["best_imperfections_score_"+str(i)][key] < -2:
                    locals()["best_imperfections_score_"+str(i)][key] = locals()["best_imperfections_score_"+str(i)][key] + 4
                elif locals()["best_imperfections_score_"+str(i)][key] >= -2 and  locals()["best_imperfections_score_"+str(i)][key] < -1:
                    locals()["best_imperfections_score_"+str(i)][key] = locals()["best_imperfections_score_"+str(i)][key] + 3.5
                elif locals()["best_imperfections_score_"+str(i)][key] >= -1 and  locals()["best_imperfections_score_"+str(i)][key] < 0:
                    locals()["best_imperfections_score_"+str(i)][key] = locals()["best_imperfections_score_"+str(i)][key] + 3
                elif locals()["best_imperfections_score_"+str(i)][key] >= 0 and  locals()["best_imperfections_score_"+str(i)][key] < 1:
                    locals()["best_imperfections_score_"+str(i)][key] = locals()["best_imperfections_score_"+str(i)][key] + 3
                elif locals()["best_imperfections_score_"+str(i)][key] >= 1 and  locals()["best_imperfections_score_"+str(i)][key] < 2:
                    locals()["best_imperfections_score_"+str(i)][key] = locals()["best_imperfections_score_"+str(i)][key] + 2.5
                elif locals()["best_imperfections_score_"+str(i)][key] >= 2 and  locals()["best_imperfections_score_"+str(i)][key] < 3:
                    locals()["best_imperfections_score_"+str(i)][key] = locals()["best_imperfections_score_"+str(i)][key] + 2
                elif locals()["best_imperfections_score_"+str(i)][key] >= 3 and  locals()["best_imperfections_score_"+str(i)][key] < 4:
                    locals()["best_imperfections_score_"+str(i)][key] = locals()["best_imperfections_score_"+str(i)][key] + 1.5
                elif locals()["best_imperfections_score_"+str(i)][key] >= 4 :
                    locals()["best_imperfections_score_"+str(i)][key] = locals()["best_imperfections_score_"+str(i)][key] + 1

            for key in locals()["best_transparency_score_"+str(i)]:				
                if locals()["best_transparency_score_"+str(i)][key] < -3 :
                    locals()["best_transparency_score_"+str(i)][key] = locals()["best_transparency_score_"+str(i)][key] + 4.5
                elif locals()["best_transparency_score_"+str(i)][key] >= -3 and  locals()["best_transparency_score_"+str(i)][key] < -2:
                    locals()["best_transparency_score_"+str(i)][key] = locals()["best_transparency_score_"+str(i)][key] + 4
                elif locals()["best_transparency_score_"+str(i)][key] >= -2 and  locals()["best_transparency_score_"+str(i)][key] < -1:
                    locals()["best_transparency_score_"+str(i)][key] = locals()["best_transparency_score_"+str(i)][key] + 3.5
                elif locals()["best_transparency_score_"+str(i)][key] >= -1 and  locals()["best_transparency_score_"+str(i)][key] < 0:
                    locals()["best_transparency_score_"+str(i)][key] = locals()["best_transparency_score_"+str(i)][key] + 3
                elif locals()["best_transparency_score_"+str(i)][key] >= 0 and  locals()["best_transparency_score_"+str(i)][key] < 1:
                    locals()["best_transparency_score_"+str(i)][key] = locals()["best_transparency_score_"+str(i)][key] + 3
                elif locals()["best_transparency_score_"+str(i)][key] >= 1 and  locals()["best_transparency_score_"+str(i)][key] < 2:
                    locals()["best_transparency_score_"+str(i)][key] = locals()["best_transparency_score_"+str(i)][key] + 2.5
                elif locals()["best_transparency_score_"+str(i)][key] >= 2 and  locals()["best_transparency_score_"+str(i)][key] < 3:
                    locals()["best_transparency_score_"+str(i)][key] = locals()["best_transparency_score_"+str(i)][key] + 2
                elif locals()["best_transparency_score_"+str(i)][key] >= 3 and  locals()["best_transparency_score_"+str(i)][key] < 4:
                    locals()["best_transparency_score_"+str(i)][key] = locals()["best_transparency_score_"+str(i)][key] + 1.5
                elif locals()["best_transparency_score_"+str(i)][key] >= 4 :
                    locals()["best_transparency_score_"+str(i)][key] = locals()["best_transparency_score_"+str(i)][key] + 1

            for key in locals()["best_sparkle_score_"+str(i)]:				
                if locals()["best_sparkle_score_"+str(i)][key] < -3 :
                    locals()["best_sparkle_score_"+str(i)][key] = locals()["best_sparkle_score_"+str(i)][key] + 4.5
                elif locals()["best_sparkle_score_"+str(i)][key] >= -3 and  locals()["best_sparkle_score_"+str(i)][key] < -2:
                    locals()["best_sparkle_score_"+str(i)][key] = locals()["best_sparkle_score_"+str(i)][key] + 4
                elif locals()["best_sparkle_score_"+str(i)][key] >= -2 and  locals()["best_sparkle_score_"+str(i)][key] < -1:
                    locals()["best_sparkle_score_"+str(i)][key] = locals()["best_sparkle_score_"+str(i)][key] + 3.5
                elif locals()["best_sparkle_score_"+str(i)][key] >= -1 and  locals()["best_sparkle_score_"+str(i)][key] < 0:
                    locals()["best_sparkle_score_"+str(i)][key] = locals()["best_sparkle_score_"+str(i)][key] + 3
                elif locals()["best_sparkle_score_"+str(i)][key] >= 0 and  locals()["best_sparkle_score_"+str(i)][key] < 1:
                    locals()["best_sparkle_score_"+str(i)][key] = locals()["best_sparkle_score_"+str(i)][key] + 3
                elif locals()["best_sparkle_score_"+str(i)][key] >= 1 and  locals()["best_sparkle_score_"+str(i)][key] < 2:
                    locals()["best_sparkle_score_"+str(i)][key] = locals()["best_sparkle_score_"+str(i)][key] + 2.5
                elif locals()["best_sparkle_score_"+str(i)][key] >= 2 and  locals()["best_sparkle_score_"+str(i)][key] < 3:
                    locals()["best_sparkle_score_"+str(i)][key] = locals()["best_sparkle_score_"+str(i)][key] + 2
                elif locals()["best_sparkle_score_"+str(i)][key] >= 3 and  locals()["best_sparkle_score_"+str(i)][key] < 4:
                    locals()["best_sparkle_score_"+str(i)][key] = locals()["best_sparkle_score_"+str(i)][key] + 1.5
                elif locals()["best_sparkle_score_"+str(i)][key] >= 4 :
                    locals()["best_sparkle_score_"+str(i)][key] = locals()["best_sparkle_score_"+str(i)][key] + 1

            for key in locals()["best_size_score_"+str(i)]:				
                if locals()["best_size_score_"+str(i)][key] < -3 :
                    locals()["best_size_score_"+str(i)][key] = locals()["best_size_score_"+str(i)][key] + 4.5
                elif locals()["best_size_score_"+str(i)][key] >= -3 and  locals()["best_size_score_"+str(i)][key] < -2:
                    locals()["best_size_score_"+str(i)][key] = locals()["best_size_score_"+str(i)][key] + 4
                elif locals()["best_size_score_"+str(i)][key] >= -2 and  locals()["best_size_score_"+str(i)][key] < -1:
                    locals()["best_size_score_"+str(i)][key] = locals()["best_size_score_"+str(i)][key] + 3.5
                elif locals()["best_size_score_"+str(i)][key] >= -1 and  locals()["best_size_score_"+str(i)][key] < 0:
                    locals()["best_size_score_"+str(i)][key] = locals()["best_size_score_"+str(i)][key] + 3
                elif locals()["best_size_score_"+str(i)][key] >= 0 and  locals()["best_size_score_"+str(i)][key] < 1:
                    locals()["best_size_score_"+str(i)][key] = locals()["best_size_score_"+str(i)][key] + 3
                elif locals()["best_size_score_"+str(i)][key] >= 1 and  locals()["best_size_score_"+str(i)][key] < 2:
                    locals()["best_size_score_"+str(i)][key] = locals()["best_size_score_"+str(i)][key] + 2.5
                elif locals()["best_size_score_"+str(i)][key] >= 2 and  locals()["best_size_score_"+str(i)][key] < 3:
                    locals()["best_size_score_"+str(i)][key] = locals()["best_size_score_"+str(i)][key] + 2
                elif locals()["best_size_score_"+str(i)][key] >= 3 and  locals()["best_size_score_"+str(i)][key] < 4:
                    locals()["best_size_score_"+str(i)][key] = locals()["best_size_score_"+str(i)][key] + 1.5
                elif locals()["best_size_score_"+str(i)][key] >= 4 :
                    locals()["best_size_score_"+str(i)][key] = locals()["best_size_score_"+str(i)][key] + 1

        #Check number of duplicate recommendations - This number will be sent to HTML
        #all_list = best_overall + best_imperfections + best_transparency +  best_sparkle +  best_size
        #dedupe_list = list(set(all_list))
        #len_diff = (len(all_list) - len(dedupe_list)) + 1

        # Write variables into the session to retrieve in the next class

        # Best rings - Is a list containing top 5 ring ID's
        session['best_overall'] = best_overall 
        session['best_imperfections'] = best_imperfections
        session['best_transparency'] = best_transparency
        session['best_sparkle'] = best_sparkle
        session['best_size'] = best_size

        # Dictionary with Key as Ring ID and raw composite score 
        # 0 - Composite, 1 - Imperfections, 2 - Transparency, 3 - Sparkle, 4 - Size
        for i in xrange(0,5):
            session['best_overall_score_%d' %i] = locals()["best_overall_score_"+str(i)]
            session['best_imperfections_score_%d' %i] = locals()["best_imperfections_score_"+str(i)]
            session['best_transparency_score_%d' %i] = locals()["best_transparency_score_"+str(i)]
            session['best_sparkle_score_%d' %i] = locals()["best_sparkle_score_"+str(i)]
            session['best_size_score_%d' %i] = locals()["best_size_score_"+str(i)]

        # Dictionary with Key as Ring ID and Price 
        session['best_overall_price'] = best_overall_price
        session['best_imperfections_price'] = best_imperfections_price
        session['best_transparency_price'] = best_transparency_price
        session['best_sparkle_price'] = best_sparkle_price
        session['best_size_price'] = best_size_price

        # Dictionary with Key as Ring ID and Merchant Description 
        session['best_overall_merchant'] = best_overall_merchant
        session['best_imperfections_merchant'] = best_imperfections_merchant
        session['best_transparency_merchant'] = best_transparency_merchant
        session['best_sparkle_merchant'] = best_sparkle_merchant
        session['best_size_merchant'] = best_size_merchant

        # Dictionary with Key as Ring ID and Product URL 
        session['best_overall_product_url'] = best_overall_product_url
        session['best_imperfections_product_url'] = best_imperfections_product_url
        session['best_transparency_product_url'] = best_transparency_product_url
        session['best_sparkle_product_url'] = best_sparkle_product_url
        session['best_size_product_url'] = best_size_product_url

        # Dictionary with Key as Ring ID and Image URL 
        session['best_overall_image_url'] = best_overall_image_url
        session['best_imperfections_image_url'] = best_imperfections_image_url
        session['best_transparency_image_url'] = best_transparency_image_url
        session['best_sparkle_image_url'] = best_sparkle_image_url
        session['best_size_image_url'] = best_size_image_url

        #session['repeat'] = len_diff
        session['cluster_title'] = cluster_title
        session['inventory_query'] = inventory_query		
        session['inventory_metal'] = inventory_metal		

class Step7(webapp2.RequestHandler):

    def get(self):
        inventory_size={}
        inventory_Sparkle = {}
        inventory_Transparency = {}
        inventory_Imperfections = {}
        inventory_price_actual = {}
        inventory_merchant = {}
        inventory_shape = {}
        inventory_setting = {}
        inventory_metal = {}
        product_url = {}
        image_url = {}
        user_shape_list = []
        user_setting_list = []
        user_ring_list = []
        session = get_current_session()
        user_setting = session.get('user_setting')
        user_setting = user_setting.upper()
        user_setting_list.append(user_setting)
        user_shape = session.get('user_shape')
        user_shape = user_shape.upper()
        user_shape_list.append(user_shape)
        user_ring = session.get('user_ring')
        user_ring = user_ring.upper()
        user_ring_list.append(user_ring)
        user_price_lower = session.get('user_price_lower')
        user_price_lower = float(user_price_lower)	
        user_price_upper = session.get('user_price_upper')
        user_price_upper = float(user_price_upper)	
        inventory_query = session.get('inventory_query')
        inventory_metal2 = session.get('inventory_metal')
        range = session.get('range')
        clus_query = session.get('clus_query')
        user_selection = session.get('user_selection')
        user_selection = int(user_selection)
        cluster_title = session.get('cluster_title')
        # Best rings - Is a list containing top n ring ID's	
        best_overall = session.get('best_overall')
        best_imperfections = session.get('best_imperfections')
        best_transparency = session.get('best_transparency')
        best_sparkle = session.get('best_sparkle')
        best_size = session.get('best_size')
        for result in inventory_query:
                inventory_size[result.count] = result.Size
                inventory_Sparkle[result.count] = result.Sparkle
                inventory_Transparency[result.count] = result.Transparency
                inventory_Imperfections[result.count] = result.Imperfections
                inventory_price_actual[result.count] = result.Price
                inventory_shape[result.count] = result.Shape
                inventory_setting[result.count] = result.Setting
                inventory_metal[result.count] = result.Metal
                product_url[result.count] = result.prod_url1
                image_url[result.count] = result.image_url1			

        # Dictionary with Key as Ring ID and raw composite score 
        # 0 - Composite, 1 - Imperfections, 2 - Transparency, 3 - Sparkle, 4 - Size

        best_overall_score_0 = session.get('best_overall_score_0')
        best_imperfections_score_0 = session.get('best_imperfections_score_0')		
        best_transparency_score_0 = session.get('best_transparency_score_0')
        best_sparkle_score_0 = session.get('best_sparkle_score_0')
        best_size_score_0 = session.get('best_size_score_0')

        best_overall_score_1 = session.get('best_overall_score_1')
        best_overall_score_1 = {str(k): v for k,v in best_overall_score_1.items()}
        best_imperfections_score_1 = session.get('best_imperfections_score_1')
        best_imperfections_score_1 = {str(k): v for k,v in best_imperfections_score_1.items()}
        best_transparency_score_1 = session.get('best_transparency_score_1')
        best_transparency_score_1 = {str(k): v for k,v in best_transparency_score_1.items()}
        best_sparkle_score_1 = session.get('best_sparkle_score_1')
        best_sparkle_score_1 = {str(k): v for k,v in best_sparkle_score_1.items()}
        best_size_score_1 = session.get('best_size_score_1')
        best_size_score_1 = {str(k): v for k,v in best_size_score_1.items()}

        best_overall_score_2 = session.get('best_overall_score_2')
        best_overall_score_2 = {str(k): v for k,v in best_overall_score_2.items()}
        best_imperfections_score_2 = session.get('best_imperfections_score_2')
        best_imperfections_score_2 = {str(k): v for k,v in best_imperfections_score_2.items()}
        best_transparency_score_2 = session.get('best_transparency_score_2')
        best_transparency_score_2 = {str(k): v for k,v in best_transparency_score_2.items()}
        best_sparkle_score_2 = session.get('best_sparkle_score_2')
        best_sparkle_score_2 = {str(k): v for k,v in best_sparkle_score_2.items()}
        best_size_score_2 = session.get('best_size_score_2')
        best_size_score_2 = {str(k): v for k,v in best_size_score_2.items()}

        best_overall_score_3 = session.get('best_overall_score_3')
        best_overall_score_3 = {str(k): v for k,v in best_overall_score_3.items()}
        best_imperfections_score_3 = session.get('best_imperfections_score_3')
        best_imperfections_score_3 = {str(k): v for k,v in best_imperfections_score_3.items()}
        best_transparency_score_3 = session.get('best_transparency_score_3')
        best_transparency_score_3 = {str(k): v for k,v in best_transparency_score_3.items()}
        best_sparkle_score_3 = session.get('best_sparkle_score_3')
        best_sparkle_score_3 = {str(k): v for k,v in best_sparkle_score_3.items()}
        best_size_score_3 = session.get('best_size_score_3')
        best_size_score_3 = {str(k): v for k,v in best_size_score_3.items()}

        best_overall_score_4 = session.get('best_overall_score_4')
        best_overall_score_4 = {str(k): v for k,v in best_overall_score_4.items()}
        best_imperfections_score_4 = session.get('best_imperfections_score_4')
        best_imperfections_score_4 = {str(k): v for k,v in best_imperfections_score_4.items()}
        best_transparency_score_4 = session.get('best_transparency_score_4')
        best_transparency_score_4 = {str(k): v for k,v in best_transparency_score_4.items()}		
        best_sparkle_score_4 = session.get('best_sparkle_score_4')
        best_sparkle_score_4 = {str(k): v for k,v in best_sparkle_score_4.items()}
        best_size_score_4 = session.get('best_size_score_4')
        best_size_score_4 = {str(k): v for k,v in best_size_score_4.items()}
        
        # Find best feature of the ring - Best Overall
        best_overall_feature = defaultdict(list)
        best_overall_index = {}
        for (key, value) in best_overall_score_1.iteritems():
            best_overall_feature[key].append(value)
        for (key, value) in best_overall_score_2.iteritems():
            best_overall_feature[key].append(value)
        for (key, value) in best_overall_score_3.iteritems():
            best_overall_feature[key].append(value)
        for (key, value) in best_overall_score_4.iteritems():
            best_overall_feature[key].append(value)
        for (key,value) in best_overall_feature.iteritems():
            best_overall_index[key] = value.index(max(value))

        # Find best feature of the ring - Best Imperfections
        best_imperfections_feature = defaultdict(list)
        best_imperfections_index = {}		
        for (key, value) in best_imperfections_score_1.iteritems():
            best_imperfections_feature[key].append(value)
        for (key, value) in best_imperfections_score_2.iteritems():
            best_imperfections_feature[key].append(value)
        for (key, value) in best_imperfections_score_3.iteritems():
            best_imperfections_feature[key].append(value)
        for (key, value) in best_imperfections_score_4.iteritems():
            best_imperfections_feature[key].append(value)
        for (key,value) in best_imperfections_feature.iteritems():
            best_imperfections_index[key] = value.index(max(value))

        # Find best feature of the ring - Best Transparency
        best_transparency_feature = defaultdict(list)
        best_transparency_index = {}		
        for (key, value) in best_transparency_score_1.iteritems():
            best_transparency_feature[key].append(value)
        for (key, value) in best_transparency_score_2.iteritems():
            best_transparency_feature[key].append(value)
        for (key, value) in best_transparency_score_3.iteritems():
            best_transparency_feature[key].append(value)
        for (key, value) in best_transparency_score_4.iteritems():
            best_transparency_feature[key].append(value)
        for (key,value) in best_transparency_feature.iteritems():
            best_transparency_index[key] = value.index(max(value))

        # Find best feature of the ring - Best Sparkle
        best_sparkle_feature = defaultdict(list)
        best_sparkle_index = {}		
        for (key, value) in best_sparkle_score_1.iteritems():
            best_sparkle_feature[key].append(value)
        for (key, value) in best_sparkle_score_2.iteritems():
            best_sparkle_feature[key].append(value)
        for (key, value) in best_sparkle_score_3.iteritems():
            best_sparkle_feature[key].append(value)
        for (key, value) in best_sparkle_score_4.iteritems():
            best_sparkle_feature[key].append(value)
        for (key,value) in best_sparkle_feature.iteritems():
            best_sparkle_index[key] = value.index(max(value))

        # Find best feature of the ring - Best Sparkle
        best_size_feature = defaultdict(list)
        best_size_index = {}		
        for (key, value) in best_size_score_1.iteritems():
            best_size_feature[key].append(value)
        for (key, value) in best_size_score_2.iteritems():
            best_size_feature[key].append(value)
        for (key, value) in best_size_score_3.iteritems():
            best_size_feature[key].append(value)
        for (key, value) in best_size_score_4.iteritems():
            best_size_feature[key].append(value)
        for (key,value) in best_size_feature.iteritems():
            best_size_index[key] = value.index(max(value))

        best_overall_index = {int(k): v for k,v in best_overall_index.items()}			
        best_imperfections_index = {int(k): v for k,v in best_imperfections_index.items()}
        best_transparency_index = {int(k): v for k,v in best_transparency_index.items()}
        best_sparkle_index = {int(k): v for k,v in best_sparkle_index.items()}
        best_size_index = {int(k): v for k,v in best_size_index.items()}

		
        # Dictionary with Key as Ring ID and Price 
        best_overall_price = session.get('best_overall_price')
        best_imperfections_price = session.get('best_imperfections_price')
        best_transparency_price = session.get('best_transparency_price')
        best_sparkle_price = session.get('best_sparkle_price')
        best_size_price = session.get('best_size_price')

        # Dictionary with Key as Ring ID and Merchant Description 
        best_overall_merchant = session.get('best_overall_merchant')
        best_imperfections_merchant = session.get('best_imperfections_merchant')
        best_transparency_merchant = session.get('best_transparency_merchant')
        best_sparkle_merchant = session.get('best_sparkle_merchant')
        best_size_merchant = session.get('best_size_merchant')

        # Dictionary with Key as Ring ID and Product URL 
        best_overall_product_url = session.get('best_overall_product_url')
        best_imperfections_product_url = session.get('best_imperfections_product_url')
        best_transparency_product_url = session.get('best_transparency_product_url')
        best_sparkle_product_url = session.get('best_sparkle_product_url')
        best_size_product_url = session.get('best_size_product_url')

        # Dictionary with Key as Ring ID and Image URL 
        best_overall_image_url = session.get('best_overall_image_url')
        best_imperfections_image_url = session.get('best_imperfections_image_url')
        best_transparency_image_url = session.get('best_transparency_image_url')
        best_sparkle_image_url = session.get('best_sparkle_image_url')
        best_size_image_url = session.get('best_size_image_url')

        template_values = {}

        # Passes to HTML the Product ID - Only Top Ring in each category
        template_values['best_ring_id'] = best_overall[0]
        template_values['purity_ring_id'] = best_imperfections[0]
        template_values['transparency_ring_id'] = best_transparency[0]
        template_values['sparkle_ring_id'] = best_sparkle[0]
        template_values['size_ring_id'] = best_size[0]	

        # Passes to HTML to fill the number of stars - Get Ring ID's scores from Session - In this page only composite score is needed
        template_values['best_ring_score_0'] = best_overall_score_0[best_overall[0]]
        template_values['purity_ring_score_0' ] = best_imperfections_score_0[best_imperfections[0]]
        template_values['transparency_ring_score_0' ] = best_transparency_score_0[best_transparency[0]]
        template_values['sparkle_ring_score_0' ] = best_sparkle_score_0[best_sparkle[0]]
        template_values['size_ring_score_0' ] = best_size_score_0[best_size[0]]

		# Index of the Key Feature of the ring
        template_values['best_ring_feature'] = best_overall_index[best_overall[0]]
        template_values['purity_ring_feature' ] = best_imperfections_index[best_imperfections[0]]
        template_values['transparency_ring_feature' ] = best_transparency_index[best_transparency[0]]
        template_values['sparkle_ring_feature' ] = best_sparkle_index[best_sparkle[0]]
        template_values['size_ring_feature' ] = best_size_index[best_size[0]]

        # Passes to HTML to show product Price - Only Top Ring in each category
        template_values['best_ring_price'] = "{:,}".format(int(best_overall_price[best_overall[0]]))
        template_values['purity_ring_price'] = "{:,}".format(int(best_imperfections_price[best_imperfections[0]])) 
        template_values['transparency_ring_price'] = "{:,}".format(int(best_transparency_price[best_transparency[0]])) 
        template_values['sparkle_ring_price'] = "{:,}".format(int(best_sparkle_price[best_sparkle[0]]))
        template_values['size_ring_price'] = "{:,}".format(int(best_size_price[best_size[0]]))

        # Passes to HTML the merchant description - Only Top Ring in each category - Excluded in New Design
        #template_values['best_ring_merchant'] = best_overall_merchant[best_overall[0]]
        #template_values['perfection_ring_merchant'] = best_imperfections_merchant[best_imperfections[0]]
        #template_values['transparency_ring_merchant'] = best_transparency_merchant[best_transparency[0]]
        #template_values['sparkle_ring_merchant'] = best_sparkle_merchant[best_sparkle[0]]
        #template_values['size_ring_merchant'] = best_size_merchant[best_size[0]]

        # Passes to HTML the Image URL - Only Top Ring in each category 
        template_values['best_ring_image_url'] = best_overall_image_url[best_overall[0]]
        template_values['purity_ring_image_url'] = best_imperfections_image_url[best_imperfections[0]]
        template_values['transparency_ring_image_url'] = best_transparency_image_url[best_transparency[0]]
        template_values['sparkle_ring_image_url'] = best_sparkle_image_url[best_sparkle[0]]
        template_values['size_ring_image_url'] = best_size_image_url[best_size[0]]

        # Convert to Upper
        selection_title = ''.join(cluster_title)
        selection_title = selection_title.upper()
        # Passes to HTML the Customer Preference from Cluster Page
        template_values['Preference'] = selection_title
        template_values['ring_metal'] = user_ring
        template_values['price'] = user_price_lower
		
        # Dictionary with Key as Ring ID and Feature Index 
        session['best_overall_index'] = best_overall_index
        session['best_imperfections_index'] = best_imperfections_index
        session['best_transparency_index'] = best_transparency_index
        session['best_sparkle_index'] = best_sparkle_index
        session['best_size_index'] = best_size_index

        # Dictionary with Key as Ring ID and Image URL 
        session['best_overall_image_url'] = best_overall_image_url
        session['best_imperfections_image_url'] = best_imperfections_image_url
        session['best_transparency_image_url'] = best_transparency_image_url
        session['best_sparkle_image_url'] = best_sparkle_image_url
        session['best_size_image_url'] = best_size_image_url
       
        # Passes to HTML the number of time as specific product overlapped in recommendations
        #template_values['Repeat'] = session.get('repeat')
        #self.response.out.write(best_imperfections_image_url)
        template = jinja_environment.get_template('step7.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        session = get_current_session()
        session['ring_selection'] = self.request.get('select') # Get the ring that was selected in the pick page
        self.redirect('/step8')

class alt7step1(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        user_ring = session.get('user_ring')
        user_price_lower = session.get('user_price_lower')
        user_price_lower = float(user_price_lower)	
        user_price_upper = session.get('user_price_upper')
        user_price_upper = float(user_price_upper)	
        user_setting = session.get('user_setting')
        user_shape = session.get('user_shape')
        range = session.get('range')
        clus_query = session.get('clus_query')
        user_selection = session.get('user_selection')
        user_selection = int(user_selection)
        cluster_title = session.get('cluster_title')
        # Best rings - Is a list containing top n ring ID's	
        best_overall = session.get('best_overall')
        best_imperfections = session.get('best_imperfections')
        best_transparency = session.get('best_transparency')
        best_sparkle = session.get('best_sparkle')
        best_size = session.get('best_size')

        # Dictionary with Key as Ring ID and raw composite score 
        # 0 - Composite, 1 - Imperfections, 2 - Transparency, 3 - Sparkle, 4 - Size

        best_overall_score_0 = session.get('best_overall_score_0')
        best_imperfections_score_0 = session.get('best_imperfections_score_0')
        best_transparency_score_0 = session.get('best_transparency_score_0')
        best_sparkle_score_0 = session.get('best_sparkle_score_0')
        best_size_score_0 = session.get('best_size_score_0')

        # Dictionary with Key as Ring ID and Price 
        best_overall_price = session.get('best_overall_price')
        best_imperfections_price = session.get('best_imperfections_price')
        best_transparency_price = session.get('best_transparency_price')
        best_sparkle_price = session.get('best_sparkle_price')
        best_size_price = session.get('best_size_price')

        # Dictionary with Key as Ring ID and Merchant Description 
        best_overall_merchant = session.get('best_overall_merchant')
        best_imperfections_merchant = session.get('best_imperfections_merchant')
        best_transparency_merchant = session.get('best_transparency_merchant')
        best_sparkle_merchant = session.get('best_sparkle_merchant')
        best_size_merchant = session.get('best_size_merchant')

        # Dictionary with Key as Ring ID and Product URL 
        best_overall_product_url = session.get('best_overall_product_url')
        best_imperfections_product_url = session.get('best_imperfections_product_url')
        best_transparency_product_url = session.get('best_transparency_product_url')
        best_sparkle_product_url = session.get('best_sparkle_product_url')
        best_size_product_url = session.get('best_size_product_url')

        # Dictionary with Key as Ring ID and Image URL 
        best_overall_image_url = session.get('best_overall_image_url')
        best_imperfections_image_url = session.get('best_imperfections_image_url')
        best_transparency_image_url = session.get('best_transparency_image_url')
        best_sparkle_image_url = session.get('best_sparkle_image_url')
        best_size_image_url = session.get('best_size_image_url')

        # Dictionary with Key as Ring ID and Feature Index 
        best_overall_index = session.get('best_overall_index')
        best_imperfections_index = session.get('best_imperfections_index')
        best_transparency_index = session.get('best_transparency_index')
        best_sparkle_index = session.get('best_sparkle_index')
        best_size_index = session.get('best_size_index')

        template_values = {}
        
        for i in xrange(1,2):
            template_values['alt_best_ring_id'] = best_overall[i]
            template_values['alt_best_score_0'] = best_overall_score_0[best_overall[i]]
            template_values['alt_best_ring_price'] = "{:,}".format(int(best_overall_price[best_overall[i]]))
            template_values['alt_best_image_url'] = best_overall_image_url[best_overall[i]]
            template_values['alt_best_feature'] = best_overall_index[best_overall[i]]
            template_values['alt_purity_ring_id'] = best_imperfections[i]
            template_values['alt_purity_score_0'] = best_imperfections_score_0[best_imperfections[i]]
            template_values['alt_purity_ring_price'] = "{:,}".format(int(best_imperfections_price[best_imperfections[i]]))
            template_values['alt_purity_image_url'] = best_imperfections_image_url[best_imperfections[i]]
            template_values['alt_purity_feature'] = best_imperfections_index[best_imperfections[i]]
            template_values['alt_transparency_ring_id'] = best_transparency[i]
            template_values['alt_transparency_score_0'] = best_transparency_score_0[best_transparency[i]]
            template_values['alt_transparency_ring_price'] = "{:,}".format(int(best_transparency_price[best_transparency[i]]))
            template_values['alt_transparency_image_url'] = best_transparency_image_url[best_transparency[i]]
            template_values['alt_transparency_feature'] = best_transparency_index[best_transparency[i]]
            template_values['alt_sparkle_ring_id'] = best_sparkle[i]
            template_values['alt_sparkle_score_0'] = best_sparkle_score_0[best_sparkle[i]]
            template_values['alt_sparkle_ring_price'] = "{:,}".format(int(best_sparkle_price[best_sparkle[i]]))
            template_values['alt_sparkle_image_url'] = best_sparkle_image_url[best_sparkle[i]]
            template_values['alt_sparkle_feature'] = best_sparkle_index[best_sparkle[i]]
            template_values['alt_size_ring_id'] = best_size[i]
            template_values['alt_size_score_0'] = best_size_score_0[best_size[i]]
            template_values['alt_size_ring_price'] = "{:,}".format(int(best_size_price[best_size[i]]))
            template_values['alt_size_image_url'] = best_size_image_url[best_size[i]]
            template_values['alt_size_feature'] = best_size_index[best_size[i]]
        template = jinja_environment.get_template('alt.html')
        self.response.out.write(template.render(template_values))

class alt7step2(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        user_ring = session.get('user_ring')
        user_price_lower = session.get('user_price_lower')
        user_price_lower = float(user_price_lower)	
        user_price_upper = session.get('user_price_upper')
        user_price_upper = float(user_price_upper)	
        user_setting = session.get('user_setting')
        user_shape = session.get('user_shape')
        range = session.get('range')
        clus_query = session.get('clus_query')
        user_selection = session.get('user_selection')
        user_selection = int(user_selection)
        cluster_title = session.get('cluster_title')
        # Best rings - Is a list containing top n ring ID's	
        best_overall = session.get('best_overall')
        best_imperfections = session.get('best_imperfections')
        best_transparency = session.get('best_transparency')
        best_sparkle = session.get('best_sparkle')
        best_size = session.get('best_size')

        # Dictionary with Key as Ring ID and raw composite score 
        # 0 - Composite, 1 - Imperfections, 2 - Transparency, 3 - Sparkle, 4 - Size

        best_overall_score_0 = session.get('best_overall_score_0')
        best_imperfections_score_0 = session.get('best_imperfections_score_0')
        best_transparency_score_0 = session.get('best_transparency_score_0')
        best_sparkle_score_0 = session.get('best_sparkle_score_0')
        best_size_score_0 = session.get('best_size_score_0')

        # Dictionary with Key as Ring ID and Price 
        best_overall_price = session.get('best_overall_price')
        best_imperfections_price = session.get('best_imperfections_price')
        best_transparency_price = session.get('best_transparency_price')
        best_sparkle_price = session.get('best_sparkle_price')
        best_size_price = session.get('best_size_price')

        # Dictionary with Key as Ring ID and Merchant Description 
        best_overall_merchant = session.get('best_overall_merchant')
        best_imperfections_merchant = session.get('best_imperfections_merchant')
        best_transparency_merchant = session.get('best_transparency_merchant')
        best_sparkle_merchant = session.get('best_sparkle_merchant')
        best_size_merchant = session.get('best_size_merchant')

        # Dictionary with Key as Ring ID and Product URL 
        best_overall_product_url = session.get('best_overall_product_url')
        best_imperfections_product_url = session.get('best_imperfections_product_url')
        best_transparency_product_url = session.get('best_transparency_product_url')
        best_sparkle_product_url = session.get('best_sparkle_product_url')
        best_size_product_url = session.get('best_size_product_url')

        # Dictionary with Key as Ring ID and Image URL 
        best_overall_image_url = session.get('best_overall_image_url')
        best_imperfections_image_url = session.get('best_imperfections_image_url')
        best_transparency_image_url = session.get('best_transparency_image_url')
        best_sparkle_image_url = session.get('best_sparkle_image_url')
        best_size_image_url = session.get('best_size_image_url')

        # Dictionary with Key as Ring ID and Feature Index 
        best_overall_index = session.get('best_overall_index')
        best_imperfections_index = session.get('best_imperfections_index')
        best_transparency_index = session.get('best_transparency_index')
        best_sparkle_index = session.get('best_sparkle_index')
        best_size_index = session.get('best_size_index')

        template_values = {}
        
        for i in xrange(2,3):
            template_values['alt_best_ring_id'] = best_overall[i]
            template_values['alt_best_score_0'] = best_overall_score_0[best_overall[i]]
            template_values['alt_best_ring_price'] = "{:,}".format(int(best_overall_price[best_overall[i]]))
            template_values['alt_best_image_url'] = best_overall_image_url[best_overall[i]]
            template_values['alt_best_feature'] = best_overall_index[best_overall[i]]
            template_values['alt_purity_ring_id'] = best_imperfections[i]
            template_values['alt_purity_score_0'] = best_imperfections_score_0[best_imperfections[i]]
            template_values['alt_purity_ring_price'] = "{:,}".format(int(best_imperfections_price[best_imperfections[i]]))
            template_values['alt_purity_image_url'] = best_imperfections_image_url[best_imperfections[i]]
            template_values['alt_purity_feature'] = best_imperfections_index[best_imperfections[i]]
            template_values['alt_transparency_ring_id'] = best_transparency[i]
            template_values['alt_transparency_score_0'] = best_transparency_score_0[best_transparency[i]]
            template_values['alt_transparency_ring_price'] = "{:,}".format(int(best_transparency_price[best_transparency[i]]))
            template_values['alt_transparency_image_url'] = best_transparency_image_url[best_transparency[i]]
            template_values['alt_transparency_feature'] = best_transparency_index[best_transparency[i]]
            template_values['alt_sparkle_ring_id'] = best_sparkle[i]
            template_values['alt_sparkle_score_0'] = best_sparkle_score_0[best_sparkle[i]]
            template_values['alt_sparkle_ring_price'] = "{:,}".format(int(best_sparkle_price[best_sparkle[i]]))
            template_values['alt_sparkle_image_url'] = best_sparkle_image_url[best_sparkle[i]]
            template_values['alt_sparkle_feature'] = best_sparkle_index[best_sparkle[i]]
            template_values['alt_size_ring_id'] = best_size[i]
            template_values['alt_size_score_0'] = best_size_score_0[best_size[i]]
            template_values['alt_size_ring_price'] = "{:,}".format(int(best_size_price[best_size[i]]))
            template_values['alt_size_image_url'] = best_size_image_url[best_size[i]]
            template_values['alt_size_feature'] = best_size_index[best_size[i]]
        template = jinja_environment.get_template('alt.html')
        self.response.out.write(template.render(template_values))

class alt7step3(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        user_ring = session.get('user_ring')
        user_price_lower = session.get('user_price_lower')
        user_price_lower = float(user_price_lower)	
        user_price_upper = session.get('user_price_upper')
        user_price_upper = float(user_price_upper)	
        user_setting = session.get('user_setting')
        user_shape = session.get('user_shape')
        range = session.get('range')
        clus_query = session.get('clus_query')
        user_selection = session.get('user_selection')
        user_selection = int(user_selection)
        cluster_title = session.get('cluster_title')
        # Best rings - Is a list containing top n ring ID's	
        best_overall = session.get('best_overall')
        best_imperfections = session.get('best_imperfections')
        best_transparency = session.get('best_transparency')
        best_sparkle = session.get('best_sparkle')
        best_size = session.get('best_size')

        # Dictionary with Key as Ring ID and raw composite score 
        # 0 - Composite, 1 - Imperfections, 2 - Transparency, 3 - Sparkle, 4 - Size

        best_overall_score_0 = session.get('best_overall_score_0')
        best_imperfections_score_0 = session.get('best_imperfections_score_0')
        best_transparency_score_0 = session.get('best_transparency_score_0')
        best_sparkle_score_0 = session.get('best_sparkle_score_0')
        best_size_score_0 = session.get('best_size_score_0')

        # Dictionary with Key as Ring ID and Price 
        best_overall_price = session.get('best_overall_price')
        best_imperfections_price = session.get('best_imperfections_price')
        best_transparency_price = session.get('best_transparency_price')
        best_sparkle_price = session.get('best_sparkle_price')
        best_size_price = session.get('best_size_price')

        # Dictionary with Key as Ring ID and Merchant Description 
        best_overall_merchant = session.get('best_overall_merchant')
        best_imperfections_merchant = session.get('best_imperfections_merchant')
        best_transparency_merchant = session.get('best_transparency_merchant')
        best_sparkle_merchant = session.get('best_sparkle_merchant')
        best_size_merchant = session.get('best_size_merchant')

        # Dictionary with Key as Ring ID and Product URL 
        best_overall_product_url = session.get('best_overall_product_url')
        best_imperfections_product_url = session.get('best_imperfections_product_url')
        best_transparency_product_url = session.get('best_transparency_product_url')
        best_sparkle_product_url = session.get('best_sparkle_product_url')
        best_size_product_url = session.get('best_size_product_url')

        # Dictionary with Key as Ring ID and Image URL 
        best_overall_image_url = session.get('best_overall_image_url')
        best_imperfections_image_url = session.get('best_imperfections_image_url')
        best_transparency_image_url = session.get('best_transparency_image_url')
        best_sparkle_image_url = session.get('best_sparkle_image_url')
        best_size_image_url = session.get('best_size_image_url')

        # Dictionary with Key as Ring ID and Feature Index 
        best_overall_index = session.get('best_overall_index')
        best_imperfections_index = session.get('best_imperfections_index')
        best_transparency_index = session.get('best_transparency_index')
        best_sparkle_index = session.get('best_sparkle_index')
        best_size_index = session.get('best_size_index')

        template_values = {}
        
        for i in xrange(3,4):
            template_values['alt_best_ring_id'] = best_overall[i]
            template_values['alt_best_score_0'] = best_overall_score_0[best_overall[i]]
            template_values['alt_best_ring_price'] = "{:,}".format(int(best_overall_price[best_overall[i]]))
            template_values['alt_best_image_url'] = best_overall_image_url[best_overall[i]]
            template_values['alt_best_feature'] = best_overall_index[best_overall[i]]
            template_values['alt_purity_ring_id'] = best_imperfections[i]
            template_values['alt_purity_score_0'] = best_imperfections_score_0[best_imperfections[i]]
            template_values['alt_purity_ring_price'] = "{:,}".format(int(best_imperfections_price[best_imperfections[i]]))
            template_values['alt_purity_image_url'] = best_imperfections_image_url[best_imperfections[i]]
            template_values['alt_purity_feature'] = best_imperfections_index[best_imperfections[i]]
            template_values['alt_transparency_ring_id'] = best_transparency[i]
            template_values['alt_transparency_score_0'] = best_transparency_score_0[best_transparency[i]]
            template_values['alt_transparency_ring_price'] = "{:,}".format(int(best_transparency_price[best_transparency[i]]))
            template_values['alt_transparency_image_url'] = best_transparency_image_url[best_transparency[i]]
            template_values['alt_transparency_feature'] = best_transparency_index[best_transparency[i]]
            template_values['alt_sparkle_ring_id'] = best_sparkle[i]
            template_values['alt_sparkle_score_0'] = best_sparkle_score_0[best_sparkle[i]]
            template_values['alt_sparkle_ring_price'] = "{:,}".format(int(best_sparkle_price[best_sparkle[i]]))
            template_values['alt_sparkle_image_url'] = best_sparkle_image_url[best_sparkle[i]]
            template_values['alt_sparkle_feature'] = best_sparkle_index[best_sparkle[i]]
            template_values['alt_size_ring_id'] = best_size[i]
            template_values['alt_size_score_0'] = best_size_score_0[best_size[i]]
            template_values['alt_size_ring_price'] = "{:,}".format(int(best_size_price[best_size[i]]))
            template_values['alt_size_image_url'] = best_size_image_url[best_size[i]]
            template_values['alt_size_feature'] = best_size_index[best_size[i]]
        template = jinja_environment.get_template('alt.html')
        self.response.out.write(template.render(template_values))

class alt7step4(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        user_ring = session.get('user_ring')
        user_price_lower = session.get('user_price_lower')
        user_price_lower = float(user_price_lower)	
        user_price_upper = session.get('user_price_upper')
        user_price_upper = float(user_price_upper)	
        user_setting = session.get('user_setting')
        user_shape = session.get('user_shape')
        range = session.get('range')
        clus_query = session.get('clus_query')
        user_selection = session.get('user_selection')
        user_selection = int(user_selection)
        cluster_title = session.get('cluster_title')
        # Best rings - Is a list containing top n ring ID's	
        best_overall = session.get('best_overall')
        best_imperfections = session.get('best_imperfections')
        best_transparency = session.get('best_transparency')
        best_sparkle = session.get('best_sparkle')
        best_size = session.get('best_size')

        # Dictionary with Key as Ring ID and raw composite score 
        # 0 - Composite, 1 - Imperfections, 2 - Transparency, 3 - Sparkle, 4 - Size

        best_overall_score_0 = session.get('best_overall_score_0')
        best_imperfections_score_0 = session.get('best_imperfections_score_0')
        best_transparency_score_0 = session.get('best_transparency_score_0')
        best_sparkle_score_0 = session.get('best_sparkle_score_0')
        best_size_score_0 = session.get('best_size_score_0')

        # Dictionary with Key as Ring ID and Price 
        best_overall_price = session.get('best_overall_price')
        best_imperfections_price = session.get('best_imperfections_price')
        best_transparency_price = session.get('best_transparency_price')
        best_sparkle_price = session.get('best_sparkle_price')
        best_size_price = session.get('best_size_price')

        # Dictionary with Key as Ring ID and Merchant Description 
        best_overall_merchant = session.get('best_overall_merchant')
        best_imperfections_merchant = session.get('best_imperfections_merchant')
        best_transparency_merchant = session.get('best_transparency_merchant')
        best_sparkle_merchant = session.get('best_sparkle_merchant')
        best_size_merchant = session.get('best_size_merchant')

        # Dictionary with Key as Ring ID and Product URL 
        best_overall_product_url = session.get('best_overall_product_url')
        best_imperfections_product_url = session.get('best_imperfections_product_url')
        best_transparency_product_url = session.get('best_transparency_product_url')
        best_sparkle_product_url = session.get('best_sparkle_product_url')
        best_size_product_url = session.get('best_size_product_url')

        # Dictionary with Key as Ring ID and Image URL 
        best_overall_image_url = session.get('best_overall_image_url')
        best_imperfections_image_url = session.get('best_imperfections_image_url')
        best_transparency_image_url = session.get('best_transparency_image_url')
        best_sparkle_image_url = session.get('best_sparkle_image_url')
        best_size_image_url = session.get('best_size_image_url')

        # Dictionary with Key as Ring ID and Feature Index 
        best_overall_index = session.get('best_overall_index')
        best_imperfections_index = session.get('best_imperfections_index')
        best_transparency_index = session.get('best_transparency_index')
        best_sparkle_index = session.get('best_sparkle_index')
        best_size_index = session.get('best_size_index')

        template_values = {}
        
        for i in xrange(4,5):
            template_values['alt_best_ring_id'] = best_overall[i]
            template_values['alt_best_score_0'] = best_overall_score_0[best_overall[i]]
            template_values['alt_best_ring_price'] = "{:,}".format(int(best_overall_price[best_overall[i]]))
            template_values['alt_best_image_url'] = best_overall_image_url[best_overall[i]]
            template_values['alt_best_feature'] = best_overall_index[best_overall[i]]
            template_values['alt_purity_ring_id'] = best_imperfections[i]
            template_values['alt_purity_score_0'] = best_imperfections_score_0[best_imperfections[i]]
            template_values['alt_purity_ring_price'] = "{:,}".format(int(best_imperfections_price[best_imperfections[i]]))
            template_values['alt_purity_image_url'] = best_imperfections_image_url[best_imperfections[i]]
            template_values['alt_purity_feature'] = best_imperfections_index[best_imperfections[i]]
            template_values['alt_transparency_ring_id'] = best_transparency[i]
            template_values['alt_transparency_score_0'] = best_transparency_score_0[best_transparency[i]]
            template_values['alt_transparency_ring_price'] = "{:,}".format(int(best_transparency_price[best_transparency[i]]))
            template_values['alt_transparency_image_url'] = best_transparency_image_url[best_transparency[i]]
            template_values['alt_transparency_feature'] = best_transparency_index[best_transparency[i]]
            template_values['alt_sparkle_ring_id'] = best_sparkle[i]
            template_values['alt_sparkle_score_0'] = best_sparkle_score_0[best_sparkle[i]]
            template_values['alt_sparkle_ring_price'] = "{:,}".format(int(best_sparkle_price[best_sparkle[i]]))
            template_values['alt_sparkle_image_url'] = best_sparkle_image_url[best_sparkle[i]]
            template_values['alt_sparkle_feature'] = best_sparkle_index[best_sparkle[i]]
            template_values['alt_size_ring_id'] = best_size[i]
            template_values['alt_size_score_0'] = best_size_score_0[best_size[i]]
            template_values['alt_size_ring_price'] = "{:,}".format(int(best_size_price[best_size[i]]))
            template_values['alt_size_image_url'] = best_size_image_url[best_size[i]]
            template_values['alt_size_feature'] = best_size_index[best_size[i]]
        template = jinja_environment.get_template('alt.html')
        self.response.out.write(template.render(template_values))

class Step8(webapp2.RequestHandler):
     
    def get(self):
        inventory_size = {}
        inventory_Sparkle = {}
        inventory_Transparency = {}
        inventory_Imperfections = {}
        inventory_price_actual = {}
        inventory_merchant = {}
        inventory_ringname = {}
        inventory_ringdesc = {}
        product_url = {}
        image_url = {}
        image_url2 = {}        
        template_values = {}
        session = get_current_session()
        if self.request.get('value') == 'apple':
            template_values = {
                'test' : 'hello'
                }
        else:    
            user_ring = session.get('user_ring')
            user_price_lower = session.get('user_price_lower')
            user_price_lower = int(user_price_lower)	
            user_price_upper = session.get('user_price_upper')
            user_price_upper = int(user_price_upper)	
            user_setting = session.get('user_setting')
            user_shape = session.get('user_shape')
            range = session.get('range')
            clus_query = session.get('clus_query')
            user_selection = session.get('user_selection')
            user_selection = int(user_selection)
            cluster_title = session.get('cluster_title')
            ring_selection = session.get('ring_selection')
            ring_selection = int(ring_selection)
            # Best rings - Is a list containing top n ring ID's	
            best_overall = session.get('best_overall')
            best_imperfections = session.get('best_imperfections')
            best_transparency = session.get('best_transparency')
            best_sparkle = session.get('best_sparkle')
            best_size = session.get('best_size')
            # Dictionary with Key as Ring ID and raw composite score 
            # 0 - Composite, 1 - Imperfections, 2 - Transparency, 3 - Sparkle, 4 - Size

            best_overall_score_0 = session.get('best_overall_score_0')
            best_imperfections_score_0 = session.get('best_imperfections_score_0')
            best_transparency_score_0 = session.get('best_transparency_score_0')
            best_sparkle_score_0 = session.get('best_sparkle_score_0')
            best_size_score_0 = session.get('best_size_score_0')
            all_items_dict = dict(best_overall_score_0.items() + best_imperfections_score_0.items() + best_transparency_score_0.items() + best_sparkle_score_0.items() + best_size_score_0.items())

            inventory_query = sample_inventory_v2.query(sample_inventory_v2.count == ring_selection).fetch()
            for result in inventory_query:
                inventory_size[result.count] = result.Size
                inventory_Sparkle[result.count] = result.Sparkle_real
                inventory_Transparency[result.count] = result.Transparency_real
                inventory_Imperfections[result.count] = result.Imperfections_real
                inventory_price_actual[result.count] = result.Price
                inventory_merchant[result.count] = result.Merchant
                inventory_ringname[result.count] = result.RingName
                inventory_ringdesc[result.count] = result.Ring_des
                product_url[result.count] = result.prod_url1
                image_url[result.count] = result.image_url1
                image_url2[result.count] = result.image_url2

            # Results Template value - Price, Overall Score, Diamond characteristics, Merchant Description for the product description
            template_values['main_score_0'] = all_items_dict[ring_selection]
            template_values['main_ring_id'] = ring_selection
            template_values['main_ring_size'] = "%s Carats" %inventory_size[ring_selection]
            template_values['main_ring_purity'] = inventory_Imperfections[ring_selection]
            template_values['main_ring_transparency'] = inventory_Transparency[ring_selection]
            template_values['main_ring_sparkle'] = inventory_Sparkle[ring_selection]
            template_values['main_ring_price'] = "{:,}".format(int(inventory_price_actual[ring_selection]))
            template_values['main_ring_merchant'] = inventory_merchant[ring_selection]
            template_values['main_ring_ringname'] = inventory_ringname[ring_selection]
            template_values['main_ring_ringdesc'] = inventory_ringdesc[ring_selection]
            template_values['main_ring_product_url'] = product_url[ring_selection]
            template_values['main_ring_image_url'] = image_url[ring_selection]

            # Review you selection template values for the new design
            template_values['shape'] = user_shape.upper()
            template_values['setting'] = user_setting.upper()
            template_values['ring_metal'] = user_ring
            template_values['user_price_lower'] = "{:,}".format(int(user_price_lower))
            template_values['user_price_upper'] = "{:,}".format(int(user_price_upper))
            template_values['cluster_title'] = cluster_title[0]
            input = user_input_db(price_lower=user_price_lower,price_upper=user_price_upper,shape=user_shape,setting=user_setting,ring_metal=user_ring,cluster_title=cluster_title[0],ring_selection=ring_selection)
            input.put()
            #self.response.out.write(product_url)
            #self.response.out.write(image_url)
        template = jinja_environment.get_template('step8.html')
        self.response.out.write(template.render(template_values))

class Test(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        channel_token = session.get('token')
        channel.send_message(channel_token, 'hello')
        self.response.out.write(channel_token)
        

class emailCheck(webapp2.RequestHandler):

    def post(self):
        user_email = self.request.get('email')
        gen_feedback = self.request.get('feedback')
        recomm_feedback = self.request.get('feedback2')
        comp_feedback = self.request.get('feedback3')
        dtype_feedback = self.request.get('feedback4')
        question_feedback = self.request.get('feedback5')
        sex = self.request.get('sex')
        married = self.request.get('married')
        ring = self.request.get('ring')
        online = self.request.get('online')
        shop_style = self.request.get('online2')
        input = email2_db(email=user_email,gen_feedback=gen_feedback,recomm_feedback=recomm_feedback,comp_feedback=comp_feedback,dtype_feedback=dtype_feedback,question_feedback=question_feedback,sex=sex,married=married,ring=ring,online=online,shop_style=shop_style)
        input.put()
        temp2 = user_email.find("@")
        temp3 = user_email.find(".",temp2)

        new_user = "Thank you for the feedback. We'll email you at " + user_email + " when we launch."
        bad_user = "Thanks for the feedback. We'll email you when we launch."
        if temp2 > -1 and temp3 > -1:
            template_values = {
                'Phrase': new_user,
            }
            template = jinja_environment.get_template('response.html')
            self.response.out.write(template.render(template_values))
        else:
            template_values = {
                'Phrase': bad_user,
                }
            template = jinja_environment.get_template('response.html')
            self.response.out.write(template.render(template_values))

class Search(webapp2.RequestHandler):

    def get(self):
        session = get_current_session()
        merchant = self.request.get("merchantName")
        #merchant = "CaratsDirect2U"
        #merchant = merchant.encode('utf-8')  
        inventory_query = sample_inventory_v2.query(sample_inventory_v2.Merchant_id == 48585).fetch()
        inventory_price_actual = {}
        inventory_merchant = {}
        inventory_shape = {}
        inventory_setting = {}
        inventory_metal = {}
        product_url = {}
        image_url = {}
        template_values = {}
        for result in inventory_query:
                inventory_price_actual[result.count] = result.Price
                inventory_shape[result.count] = result.Shape
                inventory_setting[result.count] = result.Setting
                inventory_merchant[result.count] = result.Merchant
                inventory_metal[result.count] = result.Metal
                product_url[result.count] = result.prod_url1
                image_url[result.count] = result.image_url1
        session['inventory_price_actual'] = inventory_price_actual
        session['inventory_merchant'] = inventory_merchant		
        session['inventory_shape'] = inventory_shape
        session['inventory_setting'] = inventory_setting
        session['inventory_metal'] = inventory_metal
        session['image_url'] = image_url
        session['product_url'] = product_url						
        template = jinja_environment.get_template("search.html")
        #self.response.out.write(inventory_merchant)
        #self.response.out.write(inventory_shape)
        #self.response.out.write(inventory_setting)
        #self.response.out.write(inventory_metal)		
        #self.response.out.write(merchant)
        self.response.out.write(template.render(template_values))
        

class Data(webapp2.RequestHandler):

    def get(self):
        session = get_current_session()
        merchant = self.request.get("merchantName")
        user_setting = []
        user_metal = []
        user_shape = []		
        user_setting = self.request.get("setting")
        user_metal = self.request.get("metal")
        user_shape = self.request.get("shape")
        inventory_price_actual = session.get("inventory_price_actual")
        inventory_merchant = session.get("inventory_merchant")
        inventory_shape = session.get("inventory_shape")
        inventory_setting = session.get("inventory_setting")
        inventory_metal = session.get("inventory_metal")
        image_url = session.get("image_url")
        product_url = session.get("product_url")
        page = self.request.get("page")
        if user_setting=="ALL":
            user_setting = ["PRONG","BEZEL"]
        if user_metal=="ALL":
            user_metal = ["WHITE","GOLD","PLATINUM"]
        if user_shape=="ALL":
            user_shape = ["ROUND","PRINCESS","MARQUISE","OVAL","CUSHION","RADIANT","HEART"]
        if user_metal=="WHITE GOLD":
            user_metal = ["WHITE"]
        for k,v in inventory_shape.items():
            if v not in user_shape:
                del inventory_shape[k]
 
        shape_list = inventory_shape.keys()

        for k,v in inventory_setting.items():
            if v not in user_setting:
                del inventory_setting[k]
 
        setting_list = inventory_setting.keys()

        for k,v in inventory_metal.items():
            if v not in user_metal:
                del inventory_metal[k]
 
        metal_list = inventory_metal.keys()
        
        for k, v in inventory_price_actual.items():
            if k not in shape_list:
                del inventory_price_actual[k]

        for k, v in inventory_price_actual.items():
            if k not in setting_list:
                del inventory_price_actual[k]

        for k, v in inventory_price_actual.items():
            if k not in metal_list:
                del inventory_price_actual[k]

        for k, v in image_url.items():
            if k not in shape_list:
                del image_url[k]

        for k, v in image_url.items():
            if k not in setting_list:
                del image_url[k]

        for k, v in image_url.items():
            if k not in metal_list:
                del image_url[k]

        for k, v in product_url.items():
            if k not in shape_list:
                del product_url[k]

        for k, v in product_url.items():
            if k not in setting_list:
                del product_url[k]

        for k, v in product_url.items():
            if k not in metal_list:
                del product_url[k]
        #page = 1
        page = int(page)
        total_product = len(inventory_price_actual)
        max_page = int(math.ceil(math.ceil(total_product)/8))
        if page < max_page:
            for j in xrange((page-1)*8,(page)*8):
                price = inventory_price_actual.values()
                img_url = image_url.values()
                prod_url = product_url.values()
                if j == (page-1)*8 :	
                    html = """<div class="col-md-3"><div class="thumbnail"><Img src = "%(image_url) s" style="border:none;padding-bottom:0;" width="144" height="144"><div style="padding:0 10px;margin-bottom:10px;">blah blah blah <p> blabh <br/>Price: %(price) d </p><a href="%(product_url) s" class="btn btn-primary" role="button" target="_blank">Purchase</a></div></div></div>""" % {"price": price[j], "image_url": img_url[j], "product_url": prod_url[j]}
                else:
                    temp = """<div class="col-md-3"><div class="thumbnail"><Img src = "%(image_url) s" style="border:none;padding-bottom:0;" width="144" height="144"><div style="padding:0 10px;margin-bottom:10px;">blah blah blah <p> blabh <br/>Price: %(price) d </p><a href="%(product_url) s" class="btn btn-primary" role="button" target="_blank" >Purchase</a></div></div></div>""" % {"price": price[j], "image_url": img_url[j], "product_url": prod_url[j]}
                    html = html+temp
        else:
            for j in xrange((page-1)*8,total_product):
                price = inventory_price_actual.values()
                img_url = image_url.values()
                prod_url = product_url.values()
                if j == (page-1)*8 :	
                    html = """<div class="col-md-3"><div class="thumbnail"><Img src = "%(image_url) s" style="border:none;padding-bottom:0;" width="144" height="144"><div style="padding:0 10px;margin-bottom:10px;">blah blah blah <p> blabh <br/>Price: %(price) d </p><a href="%(product_url) s" class="btn btn-primary" role="button" target="_blank">Purchase</a></div></div></div>""" % {"price": price[j], "image_url": img_url[j], "product_url": prod_url[j]}
                else:
                    temp = """<div class="col-md-3"><div class="thumbnail"><Img src = "%(image_url) s" style="border:none;padding-bottom:0;" width="144" height="144"><div style="padding:0 10px;margin-bottom:10px;">blah blah blah <p> blabh <br/>Price: %(price) d </p><a href="%(product_url) s" class="btn btn-primary" role="button" target="_blank" >Purchase</a></div></div></div>""" % {"price": price[j], "image_url": img_url[j], "product_url": prod_url[j]}
                    html = html+temp

        #max_page = int(math.ceil(math.ceil(len(price))/8))
        if max_page > 1:
            if max_page > (page+4) :
                for j in xrange((page-1),(page+4)):
                    num = j + 1
                    if j == page-1:	
                        html2 = """<li class="active" name="pg"><a>%(num)d</a></li>""" % {"num": num}
                    else:
                        temp = """<li name="pg"><a>%(num)d</a></li>""" % {"num": num}
                        html2 = html2+temp
                top = """<div class="col-md-12" style="text-align:center;" name="multipage"><ul class="pagination"><li name="backpg"><a href="#"><span class="glyphicon glyphicon-chevron-left"></span></a></li>"""
                bottom = """<li name="forwardpg"><a href="#"><span class="glyphicon glyphicon-chevron-right"></span></a></li></ul></div>"""
                html2 = top+html2+bottom 
            else:
                for j in xrange((page-1),max_page):
                    num = j + 1
                    if j == page-1:	
                        html2 = """<li class="active" name="pg"><a>%(num)d</a></li>""" % {"num": num}
                    else:
                        temp = """<li name="pg"><a>%(num)d</a></li>""" % {"num": num}
                        html2 = html2+temp
                top = """<div class="col-md-12" style="text-align:center;" name="multipage"><ul class="pagination"><li name="backpg"><a href="#"><span class="glyphicon glyphicon-chevron-left"></span></a></li>"""
                bottom = """<li name="forwardpg"><a href="#"><span class="glyphicon glyphicon-chevron-right"></span></a></li></ul></div>"""
                html2 = top+html2+bottom 
        template_values = {
            "one" : html,
            "two" : html2,
            "page" : page,
            "total_product" : total_product,
            "max_pages" : max_page,
            "user_setting" : user_setting[0],
            "user_shape" : user_shape[0],
            "user_metal" : user_metal[0]
            }
        self.response.write(json.dumps(template_values))
       
class Braintree(webapp2.RequestHandler):

    def get(self):
        template = jinja_environment.get_template("braintree.html")
        braintree.Configuration.use_unsafe_ssl = True
        braintree.Configuration.configure(braintree.Environment.Sandbox,
            merchant_id='8msf5ngq2bmmx83r',
            public_key='7jrfwk7vnvqtzytz',
            private_key='3b8b6a2792577e51fc5658be05cfba56',
        )
        # For new users
        template_values = {}
        result = braintree.ClientToken.generate()
        #self.response.out.write(result)
        template_values['result'] = result
        self.response.out.write(template.render(template_values))

class CreateTransaction(webapp2.RequestHandler):

    def post(self):
        result = braintree.Transaction.sale({
            "amount": "10",
            "payment_method_none": self.request.form["payment_method_nonce"]
            
        })
        if result.is_success:
            return "<h1>Success! Transaction ID: {0}</h1>".format(result.transaction.id)
        else:
            return "<h1>Error: {0}</h1>".format(result.message)
    if __name__ == '__main__':
        app.run(debug=True)

            
application = webapp2.WSGIApplication([
('/', Step1),
('/step1', Step1),
('/step2', Step2),
('/step3', Step3),
('/step4', Step4),
('/step5', Step5),
('/step6', Step6),
('/step7', Step7),
('/alt7step1', alt7step1),
('/alt7step2', alt7step2),
('/alt7step3', alt7step3),
('/alt7step4', alt7step4),
('/emailcheck', emailCheck),
('/step8', Step8),
('/search', Search),
('/data', Data),
('/test', Test),
('/braintree', Braintree),
('/create_transaction', CreateTransaction),
], debug=True)
#important to write a 404 page response, to have it push to the blog with a contact info about something that went wrong
