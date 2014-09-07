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
from google.appengine.api import mail

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'html')))  #editing the path location of the template files

class event_db(ndb.Model):
    unique_id=ndb.StringProperty(indexed=True)
    event_type =  ndb.StringProperty(indexed=True)
    event_value = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class voting_db(ndb.Model):
    unique_id = ndb.StringProperty(indexed=True)
    product_id =  ndb.IntegerProperty(indexed=True)
    upvote_count = ndb.IntegerProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

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

class new_inventory(ndb.Model):
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
    image_url2 = ndb.StringProperty(indexed=True)
    image_url3 = ndb.StringProperty(indexed=True)
    votes = ndb.IntegerProperty(indexed=True)

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

class appointment_db(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    first_name = ndb.StringProperty(indexed=True) 
    last_name = ndb.StringProperty(indexed=True) 
    phone_number = ndb.StringProperty(indexed=True) 
    message_body = ndb.StringProperty(indexed=True) 
    appointment_time = ndb.StringProperty(indexed=True) 

class Step1(webapp2.RequestHandler):

    def get(self):
        session = get_current_session()
        unique_id = uuid.uuid4()
        c = session.get('count', 0) # I dont' fully understand why a get() function needs to be initalized if no cookie available
        session['count'] = c + 1
        template = jinja_environment.get_template('step1.html')
        self.response.out.write(template.render())
        session['unique_id'] = unique_id

class Step2(webapp2.RequestHandler):

    def post(self):
        session = get_current_session()
        internalCounter = self.request.get('internalCounter')
        user_setting = self.request.get('setting')
        unique_id = session.get('unique_id')
        unique_id = str(unique_id)
        event_type = 'Ring setting'
        session['user_setting'] = user_setting
        session['internalCounter'] = internalCounter
        input = event_db(unique_id=unique_id,event_type=event_type,event_value=user_setting)
        input.put()

class Step3(webapp2.RequestHandler):

    def post(self):
        session = get_current_session()
        user_metal = self.request.get('ring')
        unique_id = session.get('unique_id')
        unique_id = str(unique_id)
        event_type = 'Ring Metal'
        session['user_metal'] = user_metal
        input = event_db(unique_id=unique_id,event_type=event_type,event_value=user_metal)
        input.put()

class Step4(webapp2.RequestHandler):

    def post(self):
        session = get_current_session()
        user_shape = self.request.get('shape')
        unique_id = session.get('unique_id')
        unique_id = str(unique_id)
        event_type = 'Diamond Shape'
        session['user_shape'] = user_shape
        input = event_db(unique_id=unique_id,event_type=event_type,event_value=user_shape)
        input.put()

class Step5(webapp2.RequestHandler):

    def post(self):
        session = get_current_session()
        user_price = self.request.get('price')
        user_price_lower,user_price_upper = user_price.split(",") 
        user_price_lower = int(user_price_lower)
        user_price_upper = int(user_price_upper)
        unique_id = session.get('unique_id')
        unique_id = str(unique_id)
        event_type = 'Budget'
        range = user_price_upper - user_price_lower 
        session['user_price_lower'] = user_price_lower
        session['user_price_upper'] = user_price_upper
        session['range'] = range
        input = event_db(unique_id=unique_id,event_type=event_type,event_value=user_price)
        input.put()

class Step6(webapp2.RequestHandler):

    def post(self):
        session = get_current_session()
        unique_id = session.get('unique_id')
        unique_id = str(unique_id)
                
        user_shape_list = []
        user_setting_list = []
        user_metal_list = []
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
        user_metal = session.get('user_metal')
        user_metal = user_metal.upper()
        user_metal_list.append(user_metal)
        event_type1 = 'Selection size'
        event_type2 = 'Selection sparklie'
        event_type3 = 'Selection purity'
        event_type4 = 'Selection transparency'
        
        user_selection_size = self.request.get('selection_size')
        user_selection_sparkle = self.request.get('selection_sparklie')
        user_selection_purity = self.request.get('selection_purity')
        user_selection_transparency = self.request.get('selection_transparency')
        
        input = event_db(unique_id=unique_id,event_type=event_type1,event_value=user_selection_size)
        input.put()
        input = event_db(unique_id=unique_id,event_type=event_type2,event_value=user_selection_sparkle)
        input.put()
        input = event_db(unique_id=unique_id,event_type=event_type3,event_value=user_selection_purity)
        input.put()
        input = event_db(unique_id=unique_id,event_type=event_type4,event_value=user_selection_transparency)
        input.put()
        
        session['user_selection_size'] = user_selection_size
        session['user_selection_sparkle'] = user_selection_sparkle
        session['user_selection_purity'] = user_selection_purity
        session['user_selection_transparency'] = user_selection_transparency

        user_selection_size = int(user_selection_size)
        user_selection_sparkle = int(user_selection_sparkle)
        user_selection_purity = int(user_selection_purity)
        user_selection_transparency = int(user_selection_transparency)

        influence_size = user_selection_size / 100    
        influence_sparkle = user_selection_sparkle / 100    
        influence_purity = user_selection_purity / 100   
        influence_transparency = user_selection_transparency / 100   

        inventory_query = new_inventory.query(new_inventory.Price >= user_price_lower,new_inventory.Price <= user_price_upper).fetch()

        inventory_size={}
        inventory_sparkle = {}
        inventory_transparency = {}
        inventory_purity = {}
        inventory_price_actual = {}
        inventory_shape = {}
        inventory_setting = {}
        inventory_metal = {}
        product_url = {}
        image_url = {}
        inventory_merchant = {}
        
        prop_size = {}
        prop_sparkle = {}
        prop_purity = {}
        prop_transparency = {}
        price_diff_model = {}
        composite_score = {}
        
        size_diff = {}
        sparkle_diff = {}
        transparency_diff = {}
        purity_diff = {}
        
        pred_carat = {}
        pred_sparkle = {}
        pred_transparency = {}
        pred_purity = {}
        pred_carat_b = {}
        pred_price = {}
        raw_total = {}

        for result in inventory_query:
                inventory_size[result.count] = result.Size
                inventory_sparkle[result.count] = result.Sparkle
                inventory_transparency[result.count] = result.Transparency
                inventory_purity[result.count] = result.Imperfections
                inventory_price_actual[result.count] = result.Price
                inventory_shape[result.count] = result.Shape
                inventory_setting[result.count] = result.Setting
                inventory_metal[result.count] = result.Metal
                product_url[result.count] = result.prod_url1
                image_url[result.count] = result.image_url1	
                inventory_merchant[result.count] = result.Merchant
            # Prediction and optimization variable creation
        for key in inventory_price_actual:
            #Parameter estimates implementation
            intercept = 5.77287
            pred_carat[key] = (1.11253*inventory_size[key])
            if inventory_sparkle[key] == 2:
                pred_sparkle[key] = -0.01036
            elif inventory_sparkle[key] == 3:
                pred_sparkle[key] = -0.034560
            elif inventory_sparkle[key] == 4:
                pred_sparkle[key] = -0.01272
            elif inventory_sparkle[key] == 5:
                pred_sparkle[key] = 0.16027
            else :
                pred_sparkle[key] =0
            if inventory_transparency[key] == 2:
                pred_transparency[key] = 0.16078
            elif inventory_transparency[key] == 3:
                pred_transparency[key] = 0.29146
            elif inventory_transparency[key] == 4:
                pred_transparency[key] = 0.37335
            elif inventory_transparency[key] == 5:
                pred_transparency[key] = 0.44596
            elif inventory_transparency[key] == 6:
                pred_transparency[key] = 0.45475
            elif inventory_transparency[key] == 7:
                pred_transparency[key] = 0.55459
            else:
                pred_transparency[key] = 0
            if inventory_purity[key] == 2:
                pred_purity[key] = 0.15460
            elif inventory_purity[key] == 3:
                pred_purity[key] = 0.29614
            elif inventory_purity[key] == 4:
                pred_purity[key] = 0.44228
            elif inventory_purity[key] == 5:
                pred_purity[key] = 0.51656 
            elif inventory_purity[key] == 6:
                pred_purity[key] = .57903
            elif inventory_purity[key] == 7:
                pred_purity[key] = 0.66721
            elif inventory_purity[key] == 8:
                pred_purity[key] = 1.03907
            else:
                pred_purity[key] = 0
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
            raw_total[key] =  pred_carat[key] + pred_sparkle[key] + pred_purity[key] + pred_transparency[key] + pred_carat_b[key]
            prop_size[key] =  (pred_carat[key] / raw_total[key])
            prop_sparkle[key] =  (pred_sparkle[key] / raw_total[key])
            prop_purity[key] =  (pred_purity[key] / raw_total[key])
            prop_transparency[key] =  (pred_transparency[key] / raw_total[key])
        
            pred_price[key] = ((math.exp(intercept + pred_carat[key] + pred_sparkle[key] + pred_purity[key] + pred_transparency[key] + pred_carat_b[key])) * (math.exp((0.3536244*0.3536244)/2)))
        
            price_diff_model[key] = ((inventory_price_actual[key] - pred_price[key])/inventory_price_actual[key]) * 100
            size_diff[key] = prop_size[key] - influence_size
            sparkle_diff[key] = prop_sparkle[key] - influence_sparkle
            transparency_diff[key] = prop_transparency[key] -  influence_transparency
            purity_diff[key] =prop_purity[key] - influence_purity
            
            composite_score[key] = abs((influence_size*size_diff[key])) + abs((influence_sparkle*sparkle_diff[key])) + abs((influence_transparency*transparency_diff[key])) +abs((influence_purity*prop_purity[key])) 

        #Scoring System Implementation
        for k,v in inventory_shape.items():
            if v not in user_shape_list[0]:
                del inventory_shape[k]
 
        shape_list = inventory_shape.keys()

        for k,v in inventory_setting.items():
            if v not in user_setting_list[0]:
                del inventory_setting[k]
 
        setting_list = inventory_setting.keys()

        for k,v in inventory_metal.items():
            if v not in user_metal_list[0]:
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

        #Sort dictionary and keep top n - Change here is more options are needed - Preserves descending order in the output dictionary
        n = len(composite_score)
        best_overall = heapq.nsmallest(n,composite_score.items(), key=operator.itemgetter(1))
        best_overall = map(operator.itemgetter(0),best_overall)


        session['best_overall'] = best_overall 
        session['inventory_query'] = inventory_query
        self.response.out.write(best_overall)           

class Step7(webapp2.RequestHandler):

    def get(self):
        session = get_current_session()
        unique_id = session.get('unique_id')
        unique_id = str(unique_id)
        inventory_size={}
        inventory_sparkle = {}
        inventory_transparency = {}
        inventory_purity = {}
        inventory_price_actual = {}
        inventory_merchant = {}
        inventory_shape = {}
        inventory_setting = {}
        inventory_metal = {}
        inventory_ringname = {}
        inventory_ringdesc = {}
        inventory_votes = {}
        product_url = {}
        image_url1 = {}
        image_url2 = {}
        image_url3 = {}
        user_shape_list = []
        user_setting_list = []
        user_ring_list = []
        template_values = {}

        user_setting = session.get('user_setting')
        user_setting = user_setting.upper()
        user_setting_list.append(user_setting)
        user_shape = session.get('user_shape')
        user_shape = user_shape.upper()
        user_shape_list.append(user_shape)
        user_metal = session.get('user_metal')
        user_metal = user_metal.upper()
        user_ring_list.append(user_metal)
        user_price_lower = session.get('user_price_lower')
        user_price_lower = float(user_price_lower)	
        user_price_upper = session.get('user_price_upper')
        user_price_upper = float(user_price_upper)	

        inventory_query = session.get('inventory_query')

        user_selection_size = session.get('user_selection_size')
        user_selection_sparkle = session.get('user_selection_sparkle')
        user_selection_purity = session.get('user_selection_purity')
        user_selection_transparency = session.get('user_selection_transparency')

        # Best rings - Is a list containing top n ring ID's	
        best_overall = session.get('best_overall')

        for result in inventory_query:
                inventory_size[result.count] = result.Size
                inventory_sparkle[result.count] = result.Sparkle
                inventory_transparency[result.count] = result.Transparency
                inventory_purity[result.count] = result.Imperfections
                inventory_price_actual[result.count] = result.Price
                inventory_shape[result.count] = result.Shape
                inventory_merchant[result.count] = result.Merchant
                inventory_setting[result.count] = result.Setting
                inventory_metal[result.count] = result.Metal
                product_url[result.count] = result.prod_url1
                image_url1[result.count] = result.image_url1
                image_url2[result.count] = result.image_url2
                image_url3[result.count] = result.image_url3
                inventory_ringname[result.count] = result.RingName			
                inventory_ringdesc[result.count] = result.Ring_des			
                inventory_votes[result.count] = result.votes	
        total_products = len(best_overall)
        pagination_number = self.request.get("pagination_counter")
        pagination_number = int(pagination_number)
        ring_selection = best_overall[pagination_number]
        event_type = "Ring impression"        
        input = event_db(unique_id=unique_id,event_type=event_type,event_value=str(ring_selection))
        input.put()
        try :
            voting_query = voting_db.query(voting_db.product_id == ring_selection).fetch()
            total_upvotes = len(voting_query)
            template_values['ring_votes'] = inventory_votes[ring_selection] + total_upvotes
        except:
            template_values['ring_votes'] = inventory_votes[ring_selection] 
            print " no new votes"
        # Collect Price			
        template_values['main_ring_id'] = ring_selection
        template_values['main_ring_size'] = "%s Carats" %inventory_size[ring_selection]
        template_values['main_ring_purity'] = inventory_purity[ring_selection]
        template_values['main_ring_transparency'] = inventory_transparency[ring_selection]
        template_values['main_ring_sparkle'] = inventory_sparkle[ring_selection]
        template_values['main_ring_price'] = "{:,}".format(int(inventory_price_actual[ring_selection]))
        template_values['main_ring_merchant'] = inventory_merchant[ring_selection]
        template_values['main_ring_ringname'] = inventory_ringname[ring_selection]
        template_values['main_ring_ringdesc'] = inventory_ringdesc[ring_selection]
        template_values['main_ring_product_url'] = product_url[ring_selection]
        image_count = 0
        try :
            
            template_values['main_ring_image_url1'] = image_url1[ring_selection]
            if template_values['main_ring_image_url1']  == "":
                image_count = image_count
            else:
                image_count = image_count + 1
        except:
            print "no Image found"
        try:
            template_values['main_ring_image_url2'] = image_url2[ring_selection]
            if template_values['main_ring_image_url2']  == "":
                image_count = image_count
            else:
                image_count = image_count + 1
        except:
            print "no second image"
        try:
            template_values['main_ring_image_url3'] = image_url3[ring_selection]
            if template_values['main_ring_image_url3']  == "":
                image_count = image_count
            else:
                image_count = image_count + 1
        except:
              print "no third image"
        template_values['image_count'] = image_count
        # Review you selection template values for the new design
        template_values['shape'] = user_shape.upper()
        template_values['setting'] = user_setting.upper()
        template_values['ring_metal'] = user_metal
        template_values['user_price_lower'] = "{:,}".format(int(user_price_lower))
        template_values['user_price_upper'] = "{:,}".format(int(user_price_upper))
        template_values['user_selection_size'] = user_selection_size
        template_values['user_selection_sparkle'] = user_selection_sparkle
        template_values['user_selection_purity'] = user_selection_purity
        template_values['user_selection_transparency'] = user_selection_transparency
        template_values['ring_votes'] = inventory_votes[ring_selection] + total_upvotes
        template_values['total_products'] = total_products
        #template = jinja_environment.get_template('step7.html')
        self.response.write(json.dumps(template_values))
        #template = jinja_environment.get_template('step7.html')
        #self.response.out.write(inventory_query)
        #self.response.out.write(template.render(template_values))

    def post(self):
        session = get_current_session()
        session['ring_selection'] = self.request.get('select') # Get the ring that was selected in the pick page
        self.redirect('/step8')

class upvotes(webapp2.RequestHandler):
    def post(self):
        session = get_current_session()
        unique_id = session.get('unique_id')
        unique_id = str(unique_id)
        main_ring_id = self.request.get("main_ring_id")
        print main_ring_id  
        main_ring_id = int(main_ring_id)
        upvote_count = 1
        input = voting_db(unique_id=unique_id,product_id=main_ring_id,upvote_count=upvote_count)
        input.put()

class email_message(webapp2.RequestHandler):

    def post(self):
        session = get_current_session()
        user_setting = session.get('user_setting').title()
        user_shape = session.get('user_shape').title()
        user_metal = session.get('user_metal').title()
        user_price_lower = session.get('user_price_lower')
        user_price_upper = session.get('user_price_upper')
        user_selection_size = session.get('user_selection_size')
        user_selection_sparkle = session.get('user_selection_sparkle')
        user_selection_purity = session.get('user_selection_purity')
        user_selection_transparency = session.get('user_selection_transparency')
        user_selection = [user_selection_size,user_selection_sparkle,user_selection_purity,user_selection_transparency]
        most_important_feature = user_selection.index(max(user_selection))
        if most_important_feature==0:
            user_preference = "The consumer indicated that the weight of the diamond was the most important feature that he was looking for"
        elif most_important_feature==1:
            user_preference = "The consumer indicated that the sparkle of the diamond was the most important feature that he was looking for"
        elif most_important_feature==2:
            user_preference = "The consumer indicated that the purity of the diamond was the most important feature that he was looking for"
        elif most_important_feature==3:
            user_preference = "The consumer indicated that the transparency of the diamond was the most important feature that he was looking for"            
        first_name = self.request.get("first_name").title()
        last_name = self.request.get("last_name").title()
        phone_number = self.request.get("phone_number")
        message_body = self.request.get("message")
        email_user = self.request.get("email")
        subject = self.request.get("subject")
        current_product_url = self.request.get("product_url")
        current_product_img1 = self.request.get("image")
        appointment_date = self.request.get("date")
        template_values = {}
        
        if last_name == "":
            last_name = "(user didn't provide a last name)"

        if phone_number == "":
            phone_number = "(user didn't provider a contact number)"

        if message_body == "":
            message_body = "(user didn't write a message)"

        template_values['first_name'] = first_name
        template_values['last_name'] = last_name
        template_values['date'] = appointment_date
        template_values['email_user'] = email_user
        template_values['subject'] = subject
        template_values['message'] = message_body
        template_values['phone_number'] = phone_number
        template_values['upper'] =  "{:,}".format(int(user_price_upper))
        template_values['lower'] =  "{:,}".format(int(user_price_lower))
        template_values['type'] = user_setting
        template_values['metal'] = user_metal
        template_values['shape'] = user_shape
        template_values['preference'] = user_preference
        template_values['item'] = current_product_url
        template_values['image'] = current_product_img1
        template_values['email_merchant'] = "David@hakimisgem.com"

        #Message to Merchant
        message_subject_merchant = "Sparklie Appointment: Scheduled for " + appointment_date
        message = mail.EmailMessage()
        message.sender = "<sparklie3@gmail.com>"
        message.to = "<David@hakimisgem.com>"
        message.bcc = "<shaw@sparklie.net>"
        merchant_template = jinja_environment.get_template('eMerchantCopy.html')
        message.html = merchant_template.render(template_values)
        message.subject = message_subject_merchant
        message.send()

        #Message to Consumer
        message_subject_consumer = "Sparklie Appointment Confirmation: You scheduled an appointment with " + " " + "on " + appointment_date
        message.to = "<" + email_user + ">"
        consumer_template = jinja_environment.get_template('eConsumerCopy.html')
        message.html = consumer_template.render(template_values)
        message.subject = message_subject_consumer
        message.send()
        input = appointment_db(email=email_user,first_name=first_name,last_name=last_name,message_body=message_body,phone_number=phone_number,appointment_time=appointment_date)
        input.put()


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
('/upvotes', upvotes),
('/braintree', Braintree),
('/create_transaction', CreateTransaction),
('/email_message', email_message),
], debug=True)
#important to write a 404 page response, to have it push to the blog with a contact info about something that went wrong
