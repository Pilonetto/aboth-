
class Globals:
    def month_name_to_num(self,month):
        if month == 'Jan':
            return '01'
        elif month == 'Fev':
            return '02'
        elif month == 'Mar':
            return '03'
        elif month == 'Abr':
            return '04'
        elif month == 'Mai':
            return '05'
        elif month == 'Jun':
            return '06'
        elif month == 'Jul':
            return '07'
        elif month == 'Ago':
            return '08'
        elif month == 'Set':
            return '09'
        elif month == 'Out':
            return '10'
        elif month == 'Nov':
            return '11'        
        else:
           return '12'
            
    def fmt_date(self, day, month, year):
        return self.month_name_to_num(month)+ '/'+ day  + '/'+ year