from flask import Flask , render_template ,request , redirect
from flask_sqlalchemy import SQLAlchemy
import requests
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Lifeloom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
dbs = SQLAlchemy(app)

# API For Calculator 
####----------------------------------
 
url = "https://fitness-calculator.p.rapidapi.com/dailycalorie"   


headers = {
	    "X-RapidAPI-Key": "5dfcfbd6e4msh8e31c00cd9df48cp1ca3d8jsn988cad6a4ab2",
	    "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
    }

# API For Exersice
####----------------------------------

url1 = "https://exercises-by-api-ninjas.p.rapidapi.com/v1/exercises"


headers1 = {
	"X-RapidAPI-Key": "5dfcfbd6e4msh8e31c00cd9df48cp1ca3d8jsn988cad6a4ab2",
	"X-RapidAPI-Host": "exercises-by-api-ninjas.p.rapidapi.com"
}

# API for 
####---------------------------------

####---------------------------------

class datab(dbs.Model):
    sno=dbs.Column(dbs.Integer,primary_key=True)
    Title=dbs.Column(dbs.String(200),nullable=False)
    des=dbs.Column(dbs.String(1000),nullable=False)
    link=dbs.Column(dbs.String(200),nullable=True)
    
    def __repr__(self)->str:
        return f"{self.Title}"
    
@app.route("/" , methods=['GET','POST'])
def homepage():
    if(request.method == "GET"):    
        run=datab.query.all()
        return render_template('index.html',run=run)
    else:
        Title=request.form.get('Title' , False)
        des=request.form.get('des',False)
        link=request.form.get('link',False)
        
        insert=datab(Title=Title,des=des,link=link)
        dbs.session.add(insert)
        dbs.session.commit()
        run=datab.query.all()
    
        return render_template('index.html',run=run)

@app.route('/delete/<int:sno>')
def delete(sno):
    record = datab.query.filter_by(sno=sno).first()
    dbs.session.delete(record)
    dbs.session.commit()
    return redirect('/')

@app.route("/Exersice")
def Exersice():
    return render_template('exersice.html')

@app.route("/calculator", methods=['GET','POST'])
def Calculator():
   
    if(request.method == "GET"):
        return render_template("Calculator.html")
    else:
        age=request.form.get('age',False)
        gender=request.form.get('gender')
        height=request.form.get('height')
        weight=request.form.get('weight')
        
        querystring = {"age":str(age),"gender":gender,"height":str(height),"weight":str(weight),"activitylevel":"level_1"}
 
        print(querystring)
       
        response = requests.get(url, headers=headers, params=querystring)
        
        BMR = response.json()['data']['BMR']
        RTR= str(BMR)
        
        # maintain weight
        MW=response.json()['data']['goals']['maintain weight']
        MW1=str(MW)
        
        # weight loss
        WL=response.json()['data']['goals']['Weight loss']['calory']
        WL1=response.json()['data']['goals']['Weight loss']['loss weight']
        WL1_1=str(WL)
        WL1_2=str(WL1)
        
        # weight gain
        WG=response.json()['data']['goals']['Weight gain']['calory']
        WG1=response.json()['data']['goals']['Weight gain']['gain weight']
        WG1_1=str(WG)
        WG1_2=str(WG1)
        
        return render_template('Calculator.html',RTR=RTR,MW1=MW1,WL1_1=WL1_1,WL1_2=WL1_2,WG1_1=WG1_1,WG1_2=WG1_2)
    
@app.route("/guidance" , methods=['GET','POST'])
def guidance():
    search1=request.args.get('sea')
    # print(search1)
    
    querystring1 = {"muscle":search1}
    response = requests.get(url1, headers=headers1, params=querystring1)
    
    # i=0
    # n=[0,1,2,3,4,5]
    
    
    # for i in n :
        
        
 
    #     Muscle=response.json()[i]['muscle']
    #     Muscle_1=str(Muscle)
    
    #     Name=response.json()[i]['name']
    #     Name_1=str(Name)
    
    #     Equipment=response.json()[i]['equipment']
    #     Equipment_1=str(Equipment)
    
    #     Difficulty=response.json()[i]['difficulty']
    #     Difficulty_1=str(Difficulty)
    
    #     Instructions=response.json()[i]['instructions']
    #     Instructions_1=str(Instructions)
        
    #     i+=i
    
    return render_template('guidance.html', response=response.json())
    
    
    # return response.json()   

if __name__ == "__main__":
    app.run(debug = True)