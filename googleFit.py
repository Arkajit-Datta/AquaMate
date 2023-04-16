import requests

class GoogleFit:
    def __init__(self) -> None:
        self.url = "https://v1.nocodeapi.com/arkajit/fit/lNbjiDyEfwRbTbft/aggregatesDatasets?dataTypeName="
        
    def get_steps(self):
        res = self._extract_data("steps_count")
        return res["steps_count"][0]["value"]
        
    def get_calories(self):
        res = self._extract_data("calories_expended")
        return res['calories_expended'][0]['value']
    
    def get_active(self):
        res = self._extract_data('active_minutes')
        return res['active_minutes'][0]['value']
    
    def get_weight(self):
        return 65
    
    def get_All_data(self, params = "steps_count,active_minutes,calories_expended"):
        res = self._extract_data(params)
        return res['active_minutes'][0]['value'],res['calories_expended'][0]['value'],res["steps_count"][0]["value"]
    
    def _extract_data(self, arg0):
        self.url += arg0
        params = {}
        r = requests.get(url=self.url, params={})
        return r.json()
    
    def predict_water_intake(self):
        weight = self.get_weight()
        exercise_mins, cals, steps = self.get_All_data()
        
        water_each_day = weight * 0.5
        return {
            "prediction": float((water_each_day + (float(exercise_mins/30)*12)) * 0.0295735),
            "steps":steps,
            "calories": cals,
            "exercise_mins": exercise_mins
        }
    
if __name__ == "__main__":
    gfit = GoogleFit()
    print(gfit.predict_water_intake())