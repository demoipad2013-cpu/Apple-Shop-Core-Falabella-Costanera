import json, math, pathlib

LINES = ['iPhone','Mac','iPad','Watch','AirPods','Accesorios']
GOALS = [70,10,10,10,15,170]

fy27_units = {1:[158,13,7,2,4,129],2:[132,21,16,10,3,183],3:[71,11,5,8,3,137],4:[62,9,8,0,3,118],
              5:[75,16,7,8,1,170],6:[63,22,5,9,-1,167],7:[33,9,11,1,1,48]}
fy27_usd = {1:[168519,9598,3572,860,616,2065],2:[128360,17841,7700,3779,393,844],3:[80016,10566,2781,3093,686,1096],
            4:[69589,11732,4201,0,573,1883],5:[83464,16773,3707,2875,229,2551],6:[69472,23197,2781,3146,-125,2812],
            7:[20595,2565,2500,0,0,343]}
fy26_units = {1:[78,7,6,6,5,153],2:[78,17,15,12,13,173],3:[45,6,6,6,5,145],4:[52,2,8,6,3,116],5:[63,7,9,4,13,147],
              6:[95,11,13,5,11,150],7:[62,10,17,12,20,163],8:[64,9,7,7,13,139],9:[79,11,22,9,12,165],10:[90,13,26,8,1,177],
              11:[132,5,9,8,3,173],12:[96,7,24,12,4,174],13:[72,17,6,5,14,161]}
fy26_usd = {1:[71207,7203,2722,1231,1075,2711],2:[57462,17375,6183,3387,2523,3030],3:[36419,8186,2577,1337,1003,2512],
            4:[42795,2639,4065,1553,553,2004],5:[52836,5607,3886,944,2730,2787],6:[70553,13295,5405,1110,1952,2863],
            7:[54432,9471,7564,3702,4201,3357],8:[51079,9106,2755,2023,2771,3049],9:[60199,12819,8376,2467,2457,3385],
            10:[69510,14941,10634,2174,212,3311],11:[102185,4535,3247,2261,492,2913],12:[72406,6616,9068,3769,835,3599],
            13:[49781,17576,3968,2197,3128,2999]}

def P(s):
    out=[]
    for part in s.split(';'):
        part=part.strip()
        if not part: continue
        b,u,m=part.split(':'); out.append([b,int(u),int(m)])
    return out

share = {
 1:{'Telefonía':P('Apple:158:169000;Samsung:74:20465;Xiaomi:34:5802;Motorola:24:4130;Honor:24:5360;Vivo:11:2140;ZTE:6:870'),
    'Computación':P('Apple:31:10000;HP:24:23753;Lenovo:15:10982;Acer:13:8491;Asus:9:5924;Samsung:1:116'),
    'Tablet':P('Apple:7:4000;Lenovo:9:3420;Samsung:8:1890;Xiaomi:4:560;Honor:2:680'),
    'Wearables':P('Apple:2:1000;Samsung:20:1493;Huawei:26:4569;Xiaomi:17:794;Garmin:2:720')},
 2:{'Telefonía':P('Apple:132:128000;Samsung:102:35324;Xiaomi:46:6949;Motorola:66:5768;Honor:44:8169;Vivo:11:1688;ZTE:7:1873'),
    'Computación':P('Apple:21:18000;HP:27:22731;Lenovo:35:24452;Acer:16:10370;Asus:23:16186'),
    'Tablet':P('Apple:16:8000;Lenovo:6:2390;Samsung:19:4640;Xiaomi:3:670;Honor:5:1181'),
    'Wearables':P('Apple:10:4000;Samsung:14:1350;Huawei:6:456;Xiaomi:12:654;Garmin:1:259')},
 3:{'Telefonía':P('Apple:71:80000;Samsung:55:17208;Xiaomi:35:4926;Motorola:21:3926;Honor:22:2940;Vivo:7:1290;ZTE:3:1100'),
    'Computación':P('Apple:11:11000;HP:14:14151;Lenovo:18:14442;Acer:8:3969;Asus:18:11862;Samsung:1:760'),
    'Tablet':P('Apple:5:3000;Lenovo:10:2814;Samsung:9:1840;Huawei:2:1360;Honor:1:240'),
    'Wearables':P('Apple:8:3000;Samsung:1:150;Huawei:20:3450;Xiaomi:17:684')},
 4:{'Telefonía':P('Apple:62:70000;Samsung:68:25653;Xiaomi:27:5719;Motorola:33:4517;Honor:24:5390;Vivo:7:1176;ZTE:1:101'),
    'Computación':P('Apple:9:12000;HP:18:17965;Lenovo:20:14559;Acer:6:4725;Asus:12:9525;Samsung:1:690'),
    'Tablet':P('Apple:8:4000;Lenovo:5:1482;Samsung:14:8990;Huawei:1:680;Honor:1:450'),
    'Wearables':P('Samsung:11:287;Huawei:28:5390;Xiaomi:9:375;Garmin:3:897')},
 5:{'Telefonía':P('Apple:75:83000;Samsung:92:22098;Xiaomi:24:4099;Motorola:5:899;Honor:22:3067;Vivo:9:3172;ZTE:2:394'),
    'Computación':P('Apple:16:17000'),
    'Tablet':P('Apple:7:4000'),
    'Wearables':P('Apple:8:3000;Samsung:15:1183;Huawei:22:3338;Xiaomi:15:452;Garmin:6:1436')},
 6:{'Computación':P('Apple:22:23000;HP:16:15090;Lenovo:19:17369;Acer:2:2410;Asus:17:19180'),
    'Tablet':P('Apple:5:3000;Lenovo:10:3100;Samsung:15:4900;Xiaomi:0:490;Huawei:1:0;Honor:2:290')},
}

inv7 = [["iPhone","iPhone 18 Pro","256 GB",28],["iPhone","iPhone 18 Pro Max","256 GB",17],["AirPods","AirPods 5 Wired","",3],["HomePod","HomePod mini (1st Gen)","",0],["Watch","Series 12","42 mm",3],["Watch","Series 12","",2],["iPhone","iPhone 18 Pro Max","512 GB",0],["iPhone","iPhone 18 Pro","512 GB",1],["Watch","Series 12","46 mm",1],["Watch","Ultra 4","",1],["iPhone","iPhone 18 Pro","",1],["AirPods","AirPods 5 Wireless","",1],["iPhone","iPhone Duo","",1],["Watch","Ultra 4","49 mm",1],["iPhone","iPhone 18 Pro Max","",0],["iPhone","iPhone 17 Pro Max","256 GB",85],["iPhone","iPhone 17 Pro Max","512 GB",1],["iPhone","iPhone 17 Pro Max","",0],["iPhone","iPhone 17 Pro","256 GB",19],["iPhone","iPhone 17 Pro","512 GB",8],["iPhone","iPhone 17 Pro","",2],["iPhone","iPhone 17 Pro","1 TB",0],["iPhone","iPhone 17","256 GB",20],["iPhone","iPhone 17","512 GB",10],["iPhone","iPhone 17","",1],["iPhone","iPhone Air","256 GB",4],["iPhone","iPhone Air","512 GB",0],["iPhone","iPhone Air","",1],["iPhone","iPhone 17e","256 GB",0],["iPhone","iPhone 16 Plus","128 GB",0],["iPhone","iPhone 16 Plus","",0],["iPhone","iPhone 16 Plus","512 GB",0],["iPhone","iPhone 16","128 GB",0],["iPhone","iPhone 16","",1],["iPhone","iPhone 16","256 GB",0],["iPhone","iPhone 16","512 GB",0],["iPhone","iPhone 16e","128 GB",2],["iPhone","iPhone 16e","256 GB",0],["iPhone","iPhone 16e","",0],["iPhone","iPhone 16e","512 GB",0],["iPhone","iPhone 15 Plus","",0],["iPhone","iPhone 15","128 GB",3],["iPhone","iPhone 15","512 GB",0],["iPhone","iPhone 15","256 GB",0],["iPhone","iPhone 11","",0],["iPhone","iPhone SE (3rd Gen)","",0],["iPad","iPad Pro","",1],["iPad","iPad Pro","256 GB",0],["iPad","iPad Air","",8],["iPad","iPad Air","128 GB",22],["iPad","iPad Mini","128 GB",3],["iPad","iPad Mini","",0],["iPad","iPad Entry","",0],["iPad","iPad Entry","128 GB",57],["iPad","iPad Entry","256 GB",1],["Watch","Ultra 3","",1],["Watch","Ultra 3","49 mm",0],["Watch","Series 11","42 mm",4],["Watch","Series 11","",0],["Watch","Series 11","46 mm",0],["Watch","Watch SE (3rd Gen)","40 mm",0],["Watch","Watch SE (3rd Gen)","44 mm",0],["Watch","Watch SE (3rd Gen)","",0],["Watch","Ultra 2","",2],["Watch","Watch SE (2nd Gen)","",1],["Watch","Series 10","",1],["Watch","Series 9","",0],["Mac","MacBook Pro 15/16","",0],["Mac","MacBook Pro 13/14","1 TB",36],["Mac","MacBook Pro 13/14","",1],["Mac","MacBook Pro 13/14","512 GB",1],["Mac","MacBook Air 15","",0],["Mac","MacBook Air 15","512 GB",3],["Mac","MacBook Air 13","",2],["Mac","MacBook Air 13","512 GB",24],["Mac","MacBook Air 13","1 TB",19],["Mac","MacBook Neo 13","256 GB",29],["Mac","MacBook Neo 13","512 GB",1],["Mac","iMac 21/24","256 GB",0],["Mac","Mac Mini","256 GB",6],["AirPods","AirPods Pro (3rd Gen)","",4],["AirPods","AirPods Pro (2nd Gen)","",0],["AirPods","AirPods (4th Gen) ANC","",1],["AirPods","AirPods (4th Gen) non-ANC","",0],["AirPods","AirPods (3rd Gen) Wired","",0],["AirPods","AirPods (2nd Gen) Wired","",0],["HomePod","HomePod (2nd Gen)","",0],["Apple TV","Apple TV 4K 3rd Gen","64 GB",0],["Apple TV","Apple TV 4K 3rd Gen","128 GB",0],["Accesorios","Connectivity Accessories","",1037],["Accesorios","Other Headsets","",570],["Accesorios","iPad Accessories","",56],["Accesorios","iPhone Accessories","",45],["Accesorios","Mac Accessories","",5],["Accesorios","Watch Accessories","",6],["Accesorios","Apple TV Accessories","",0],["Accesorios","App-Enabled Accessories","",110]]

mu7 = [["iPhone 18 Pro Max","256 GB",8],["iPhone 18 Pro","256 GB",5],["AirPods 5 Wired","",1],["iPhone Duo","256 GB",1],["iPhone 18 Pro Max","512 GB",2],["iPhone 17 Pro Max","256 GB",5],["iPhone 17 Pro","256 GB",4],["iPhone 17","256 GB",6],["iPhone 16 Pro Max","",1],["iPhone 16 Pro","",1],["iPad Pro","",1],["iPad Air","128 GB",2],["iPad Entry","128 GB",7],["iPad Entry","256 GB",1],["Watch SE (3rd Gen)","44 mm",1],["MacBook Pro 13/14","",1],["MacBook Pro 13/14","1 TB",1],["MacBook Pro 13/14","512 GB",1],["MacBook Neo 13","512 GB",1],["MacBook Neo 13","256 GB",5],["Connectivity Accessories","",26],["Other Headsets","",19],["iPad Accessories","",1],["App-Enabled Accessories","",2]]

sum4 = {"AirPods (4th Gen) ANC|":1,"AirPods 5 Wireless|":-1,"AirPods Pro (3rd Gen)|":6,"App-Enabled Accessories|":19,"Connectivity Accessories|":364,"Mac Accessories|":1,"MacBook Air 13|":-1,"MacBook Air 13|1 TB":2,"MacBook Air 13|512 GB":22,"MacBook Air 15|512 GB":6,"MacBook Neo 13|256 GB":17,"MacBook Neo 13|512 GB":10,"MacBook Pro 13/14|":-1,"MacBook Pro 13/14|1 TB":3,"Other Headsets|":200,"Series 10|":1,"Series 11|42 mm":1,"Series 12|42 mm":5,"Series 12|46 mm":5,"Ultra 3|49 mm":1,"Ultra 4|49 mm":1,"Watch SE (2nd Gen)|":2,"Watch SE (3rd Gen)|40 mm":9,"iPad Accessories|":2,"iPad Air|128 GB":6,"iPad Entry|128 GB":12,"iPad Entry|256 GB":6,"iPad Mini|128 GB":1,"iPhone 13|":1,"iPhone 14|":1,"iPhone 15|128 GB":13,"iPhone 16 Plus|512 GB":1,"iPhone 16 Pro Max|":1,"iPhone 16 Pro|":1,"iPhone 16e|128 GB":5,"iPhone 16e|512 GB":1,"iPhone 16|128 GB":2,"iPhone 17 Pro Max|256 GB":28,"iPhone 17 Pro Max|512 GB":1,"iPhone 17 Pro|256 GB":49,"iPhone 17 Pro|512 GB":1,"iPhone 17e|256 GB":-1,"iPhone 17|256 GB":58,"iPhone 17|512 GB":6,"iPhone 18 Pro Max|":1,"iPhone 18 Pro Max|256 GB":48,"iPhone 18 Pro|256 GB":39,"iPhone 18 Pro|512 GB":2,"iPhone Accessories|":6,"iPhone Air|512 GB":5,"iPhone Duo|256 GB":8}
sug7 = {k: math.ceil(v/4) if v>0 else 0 for k,v in sum4.items()}

weeks = {}
for w in range(1,14):
    d = {'goals':list(GOALS)}
    if w in fy27_units:
        d['units']=fy27_units[w]; d['usd']=fy27_usd[w]; d['partial']= (w==7)
    if w in share: d['share']=share[w]
    weeks[f'27-1-{w}']=d
for w in range(1,14):
    weeks[f'26-1-{w}']={'goals':list(GOALS),'units':fy26_units[w],'usd':fy26_usd[w],'partial':False}
weeks['27-1-7']['inv']=inv7
weeks['27-1-7']['mu']=mu7
weeks['27-1-7']['sug']=sug7
weeks['27-1-7']['invRef']='10 Nov 2026 13:10 · AMR · parcial'

pg_pending = ['desktop-sign','imac','ipad-mini','mac-air','mac-neo','mac-pro-m6','mac-pro-xdr','neo-sign','watch-se44','xdr-sign']
REAR = ['watch-se40','watch-se44','watch-s42','watch-s46','watch-ultra','watch-sign','homepod','homepod-sign','mac-pro-xdr','mac-pro-m6','xdr-sign','mac-air','mac-neo','neo-sign','imac','desktop-sign','rear-graphic']
FRONT = ['ipad-mini','ipad-a16','ipad-air','ipad-pro','ipad-sign','airpods','airpods-sign','iphone-17e','iphone-17','iphone-air','iphone-17pro','iphone-18pro','iphone-18max','iphone-duo','iphone-comp','iphone-sign','front-graphic']
pg = {k:{'status':'Pendiente' if k in pg_pending else 'Exhibido','reason':'','note':'','action':'','owner':''} for k in REAR+FRONT}

team = [["Christopher Mendez","Vendedor/a","Telefonía"],["Sebastian Soto","Vendedor/a","Computación"],["Sebastian Durán","Vendedor/a","Computación"],["Gelen Parra","Apple Champion","Telefonía"],["Tamara Estrada","Mac Expert","Computación"],["Enrique Pilar","Promotor","Computación"],["Matias Pinto","Promotor","Computación"],["Jasson Guerra","Vendedor/a","Computación"],["Nicole Gonzalez","Vendedor/a","Telefonía"],["Karen Guillen","Vendedor/a","Telefonía"],["Kevin Taico","Vendedor/a","Audio"],["Giovanni","Vendedor/a","Telefonía"],["Cristian Sobarzo","Vendedor/a","Telefonía"],["Paula","Vendedor/a","Audio"],["Joaquin","Vendedor/a","Audio"],["David","Promotor",""]]
members = [{'id':f'm{i+1}','name':n,'role':r,'area':a,'active': n!='David'} for i,(n,r,a) in enumerate(team)]
idof = {m['name']:m['id'] for m in members}
UPD={'Christopher Mendez':('Christopher Méndez','Apple Champion','Telefonía'),'Sebastian Soto':('Sebastián Soto','Apple Champion','Computación'),'Sebastian Durán':('Sebastián Durán','Apple Champion','Computación'),'Gelen Parra':('Gelen Parra','Apple Champion · Mac Expert','Telefonía'),'Tamara Estrada':('Tamara Estrada','Mac Expert','Computación'),'Enrique Pilar':('Enrique Pilar','Promotor Full Time','Programa Apple'),'Matias Pinto':('Matías Pinto','Promotor Part Time','Programa Apple'),'Jasson Guerra':('Jasson Guerra','Vendedor/a','Computación'),'Nicole Gonzalez':('Nicol González','Vendedor/a','Telefonía'),'Karen Guillen':('Karen Guillén','Vendedor/a','Telefonía'),'Kevin Taico':('Kevin Taico','Vendedor/a','Audio'),'Giovanni':('Giovanni Lavanderos','Vendedor/a','Telefonía'),'Cristian Sobarzo':('Cristian Sobarzo','Vendedor/a','Telefonía'),'Paula':('Paula','Vendedor/a','Audio'),'Joaquin':('Joaquín','Vendedor/a','Audio')}
ORD=['Christopher Mendez','Sebastian Durán','Gelen Parra','Sebastian Soto','Tamara Estrada','Enrique Pilar','Matias Pinto','Jasson Guerra','Karen Guillen','Nicole Gonzalez','Giovanni','Cristian Sobarzo','Paula','Joaquin','Kevin Taico','David']
for m in members:
    if m['name'] in UPD: m['name'],m['role'],m['area']=UPD[m['name']]
members.sort(key=lambda m:[UPD.get(k,(k,))[0] for k in ORD].index(m['name']) if m['name'] in [UPD.get(k,(k,))[0] for k in ORD] else 99)

def ev(name,start,end,label,lines,impact,cq):
    return {'id':'e'+str(abs(hash(name))%100000),'name':name,'start':start,'end':end,'label':label,'lines':lines,'impact':impact,'cq':cq}
events = [
 ev('CyberMonday Chile','2026-10-05','2026-10-07','05-07 oct 2026','iPhone, Mac, iPad','Muy alto',1),
 ev('Singles Day 11.11','2026-11-11','2026-11-11','11 nov 2026','Accesorios, AirPods','Medio',1),
 ev('Black Week','2026-11-23','2026-11-30','23-30 nov 2026','iPhone, Watch, AirPods','Muy alto',1),
 ev('Black Friday Chile','2026-11-27','2026-11-30','27-30 nov 2026','iPhone, Mac, AirPods','Muy alto',1),
 ev('Cyber Monday internacional','2026-11-30','2026-11-30','30 nov 2026','Tecnología','Alto',1),
 ev('Navidad','2026-12-01','2026-12-24','01-24 dic 2026','AirPods, Watch, Accesorios','Muy alto',1),
 ev('Post Navidad / fin de año','2026-12-26','2026-12-31','26-31 dic 2026','Accesorios, iPhone','Alto',1),
 ev('Rebajas de verano','2027-01-01','2027-01-31','Enero 2027','iPhone, Accesorios','Medio',2),
 ev('Back to School','2027-01-01','2027-03-31','Enero-marzo 2027','Mac, iPad','Muy alto',2),
 ev('San Valentín','2027-02-14','2027-02-14','14 feb 2027','AirPods, Watch','Medio',2),
 ev('Back to University','2027-02-01','2027-03-31','Febrero-marzo 2027','Mac, iPad','Muy alto',2),
 ev('Regreso a clases','2027-03-01','2027-03-31','Marzo 2027','Mac, iPad','Alto',2),
 ev('Semana Santa','2027-03-26','2027-03-28','26-28 mar 2027','Accesorios','Medio',3),
 ev('Campañas de otoño','2027-04-01','2027-04-30','Abril 2027','Mac, iPad','Medio',3),
 ev('Día de la Madre','2027-05-09','2027-05-09','09 may 2027','Watch, AirPods','Alto',3),
 ev('CyberDay Chile','2027-05-31','2027-06-02','Fin mayo-inicio junio 2027','iPhone, Mac, iPad','Muy alto',3),
 ev('WWDC Apple','2027-06-07','2027-06-11','Junio 2027','Mac, ecosistema','Alto',3),
 ev('Día del Padre','2027-06-20','2027-06-20','20 jun 2027','Watch, AirPods','Alto',3),
 ev('Vacaciones de invierno','2027-07-01','2027-07-31','Julio 2027','iPad, Accesorios','Medio',4),
 ev('Día del Niño','2027-08-08','2027-08-08','08 ago 2027','iPad, AirPods','Alto',4),
 ev('Campañas de primavera','2027-08-01','2027-09-30','Agosto-septiembre 2027','iPhone, Accesorios','Medio',4),
 ev('Temporada NPI Apple','2027-09-01','2027-09-30','Septiembre 2027','iPhone, Watch','Muy alto',4),
 ev('Fiestas Patrias','2027-09-18','2027-09-19','18-19 sep 2027','iPhone, Accesorios','Alto',4),
]
for i,e in enumerate(events): e['id']=f'e{i+1}'

state = {
 'version':'3.0','savedAt':'2026-11-13T22:45:00-03:00','fyList':[27,28,29,30],
 'weeks':weeks,
 'promoters':{'Apple':2,'Honor':3,'Huawei':1,'Motorola':1,'Samsung':3,'Vivo':2,'Xiaomi':2,'ZTE':1},
 'insights':[json.load(open('/home/claude/dashboard-v3/seed_insight.json'))],
 'planogram':{'27-1':pg},
 'members':members,
 'formation':{'27-1-7':{idof['Christopher Mendez']:['coach-monthly','coach-t3','demo-practice','demo-participate','ops-clean','demo-success','ops-restock','demo-attend'],
                         idof['Sebastian Soto']:['coach-monthly','coach-ignite','demo-practice','ops-restock'],
                         idof['Matias Pinto']:['demo-participate','demo-success','demo-practice']}},
 'pills':{'27-1-7':[idof['Christopher Mendez']]},
 'npiItems':['iPhone 18 Pro y Pro Max','iPhone Duo','Apple Watch Series 12','Apple Watch Ultra 4','AirPods 5','MacBook Neo'],
 'npi':{},
 'lost':[{'id':'l1','key':'27-1-7','category':'Watch','model':'Apple Watch SE','capacity':'40 mm','units':1,'perception':'Buscó alternativas en el mall','escalation':'Sin escalar','note':''}],
 'escalation':{},
 'events':events,
 'checks':{},
 'actions':[],'promoActions':[],'promos':[],'compObs':[],'skus':[],
}

tpl = pathlib.Path('/home/claude/dashboard-v3/template.html').read_text()
js = json.dumps(state, ensure_ascii=False, separators=(',',':')).replace('</','<\\/')
import base64
def b64(f): return 'data:image/jpeg;base64,'+base64.b64encode(open('/home/claude/pg/'+f,'rb').read()).decode()
assets=json.dumps({'table':b64('table.jpg'),'gr':b64('gr.jpg'),'gf':b64('gf.jpg')})
out = tpl.replace('__STATE__', js).replace('__ASSETS__', assets)
pathlib.Path('/home/claude/dashboard-v3/index.html').write_text(out)
print(len(out))
