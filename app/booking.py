from flask_restful import Resource, Api,reqparse
from datetime import datetime ,timedelta
from .controller import create_reservation,get_reservation,get_guest_id
from app import app


api = Api(app)
RESTAURANT_OPEN_TIME=16
RESTAURANT_CLOSE_TIME=22

class index(Resource):
  def post(self):
    data = reqparse.RequestParser()
    data.add_argument('reservation_datetime',type=str,required=True,default=datetime.now())
    data.add_argument('guest_name',type=str,required=True)
    data.add_argument('guest_phone',type=int,required=True)   
    data.add_argument('num_guests',type=int,required=True)
    data.add_argument('email_id',type=str,required=True)
    
    print("Time Now:",datetime.now())
    
    args = data.parse_args()
    args['reservation_datetime'] = datetime.strptime(args['reservation_datetime'],'%m%d%Y %H:%M:%S')
    if args['reservation_datetime'] < datetime.now():
      return {"message": "requested data","result":"You cannot book dates in the past"},200
    
    reservation_date = datetime.combine(args['reservation_datetime'], datetime.min.time())
    
    if args['reservation_datetime'] < reservation_date + timedelta(hours=RESTAURANT_OPEN_TIME) or \
        args['reservation_datetime'] > reservation_date + timedelta(hours=RESTAURANT_CLOSE_TIME):
            
            return {"message": "requested data","result":"The restaurant is closed at that hour!"},200
    reservation = create_reservation(args)
    
   
    if reservation == 'capacity':            
            return {"message": "Request Status","result":"No tables with that size"},200
           
    elif not reservation:      
      return {"message": "Request Status","result":"That time is taken!  Try another time"},201
  
    get_guest_data= get_guest_id(args)
    return {"message": "Request Status","result":{"Status":"Confirmed","guest_name":get_guest_data.name,"guest_id":get_guest_data.id}},201
 
class booking(Resource):
  def get(self,num):
    reservation = get_reservation(num)
    if reservation:
      return {"message": "Requested Data","result":{"guest_id": reservation.guest_id ,"no_of_guests": reservation.num_guests}},200
    else:      
      return {"message": "Requested Data","result": 'no reservation with that confirmation number'},200
api.add_resource(index,'/')
api.add_resource(booking, '/booking/<int:num>')



