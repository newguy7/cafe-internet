from flask import Flask, render_template,redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField,TimeField, SelectField
from wtforms.validators import DataRequired
import csv
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])    
    location_url = URLField('Location URL', validators=[DataRequired()])
    open_time = TimeField('Open TIme', validators=[DataRequired()])
    close_time = TimeField('Close Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=["☕","☕☕","☕☕☕","☕☕☕☕","☕☕☕☕☕"], validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Rating', choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"],validators=[DataRequired()])
    power_outlet_rating = SelectField('Power Outlet Rating', choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["Get", "post"])
def add_cafe():
    form = CafeForm()
    form_data = []
    if form.validate_on_submit():
        print("True")
        cafe_data = form.cafe.data
        location_data = form.location_url.data
        open_data = form.open_time.data.strftime("%I:%M%p")
        
        close_data = form.close_time.data.strftime("%I:%M%p")
        
        coffee_data = form.coffee_rating.data
        wifi_data = form.wifi_rating.data
        power_data = form.power_outlet_rating.data
        
        with open('cafe-data.csv',newline='',mode='a',encoding='utf-8') as file: 
            file.write(f"\n{cafe_data},"
                       f"{location_data},"
                       f"{open_data},"
                       f"{close_data},"
                       f"{coffee_data},"
                       f"{wifi_data},"
                       f"{power_data}")
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        
        for row in csv_data:            
            
            list_of_rows.append(row)       
        
    return render_template('cafes.html', cafes=list_of_rows)






if __name__ == "__main__":
    app.run(debug=True)