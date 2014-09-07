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
        user_setting = self.request.get('setting')
        next = self.request.get('next')
        session['user_setting'] = user_setting
        if back =="back":
            self.redirect('/step2')
        elif next == "next":
            if user_setting != "":
                self.redirect('/step3')
            else: 
                self.redirect('/step2')


class Step3(webapp2.RequestHandler):

    def get(self):
        template = jinja_environment.get_template('step3.html')
        self.response.out.write(template.render())
        #self.redirect('html/step2.html')

    def post(self):
        session = get_current_session()
        user_ring = self.request.get('ring')
        next = self.request.get('next')
        back = self.request.get('back')
        session['user_ring'] = user_ring
        if back =="back":
            self.redirect('/step2')
        elif next == "next":
            if user_ring != "":
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
            self.redirect('/step3')
        elif next == "next":
            if user_price_lower != "" and user_price_upper != "" and range <= 2500:
                self.redirect('/step5')
            else: 
                self.redirect('/step4')

class Step5(webapp2.RequestHandler):

    def get(self):
        template = jinja_environment.get_template('step5.html')
        self.response.out.write(template.render())

    def post(self):
        session = get_current_session()
        user_shape = self.request.get('shape')
        session['user_shape'] = user_shape


