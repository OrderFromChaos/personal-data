### Imports
import os
import datetime
from bs4 import BeautifulSoup # html parsing, implicit lxml import
import matplotlib.pyplot as plt
from collections import Counter # Used for frequency charting

### Hyperparameters (you can modify these)
source_dir = '/mnt/e4763822-652b-4db6-ad99-f079b3ec54b5/Projects/Datasets/Personal Data/Facebook Data/messages'
graphs = [['Top',7],
          ['Overall']]
joined_fb = datetime.datetime(year=2008,month=10,day=26)
# graph_context accepts datetime.datetime() objects
graph_context = [[joined_fb,'Joined Facebook (2008)'],
                 [datetime.datetime(year=2014-4,month=8,day=20),'8th grade'],
                 [datetime.datetime(year=2014-3,month=8,day=20),'Freshman HS'],
                 [datetime.datetime(year=2014-2,month=8,day=20),'Sophomore HS'],
                 [datetime.datetime(year=2014-1,month=8,day=20),'Junior HS'],
                 [datetime.datetime(year=2014,month=8,day=20),'Senior HS'],
                 [datetime.datetime(year=2015,month=8,day=21),'Started UARK'],
                 [datetime.datetime(year=2016,month=9,day=24),'Started at UCR']]
dx = 10 # Change this value if the annotations on vertical lines are in the wrong place (not likely)



# Parses all the files
def pull_data(source_dir):
    '''Gets timestamps and recipients for each file in the messages source directory'''
    messenger_files = os.listdir(source_dir)
    messenger_files = [x for x in messenger_files if x[:-6:-1][::-1] == '.html'] # Cut to html files
    def parse_message_subhistory(file_name,source_dir):
        '''Does the hard work of actually getting the data (per file)'''
        if source_dir[-1] == '/': # For accessibility
            open_name = source_dir + file_name
        else:
            open_name = source_dir + '/' + file_name
        with open(open_name,'r') as f:
            # Now that we have html, throw at beautifulsoup
            raw_html = f.read()
        parsed = BeautifulSoup(raw_html,'lxml')
        conversation_with = ' '.join(parsed.find('title').text.split(' ')[2:])
        timestamps = [x.text for x in parsed.findAll(attrs={'class':'meta'})]
        # timestamps are currently in "Saturday, October 28, 2017 at 10:00pm PDT" format
        # now place it in a datetime.datetime class
        # intermediate array first
        timestamps = [x.split(' ') for x in timestamps]
        # now in format ['Saturday,', 'October', '28,', '2017', 'at', '10:00pm', 'PDT']
        month_to_num = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
        days_of_week = {'Saturday,','Sunday,','Monday,','Tuesday,','Wednesday,','Thursday,','Friday,'}
        timestamps = [datetime.datetime(year=int(x[3]),
                                    month=month_to_num[x[1]],
                                    day=int(x[2][:-1]),
                                    hour=int(x[5].split(':')[0]),
                                    minute=int(x[5].split(':')[1][:-2])) for x in timestamps if x[0] in days_of_week] # Going to ignore timezones for right now
                                                                             # it doesn't seem like datetime likes 'UTC' or 'PDT' as an input for tzinfo=...
                                                                             # also s/o to Facebook for putting emoji messages under a "meta" div class...
        return [conversation_with,timestamps]
    return [parse_message_subhistory(x,source_dir) for x in messenger_files]
info = pull_data(source_dir)
print('Data successfully imported!')

def list_names(dataset):
    # Will list names by number of messages sent
    print_list = sorted([[len(x[1]),x[0]] for x in dataset])[::-1]
#    for i in print_list:
#        print(i)
    return print_list

def graph_history(name_list,dataset,joined_fb):
    # Now supports names as a list
    names = [x[0] for x in dataset]
    largest_max = 0
    def subplot(name,dataset,joined_fb,largest_max): # __VERY__ lazy way of extending functionality
        loc = names.index(name)
        days_since_joining = (datetime.datetime.now()-joined_fb).days
        if loc != -1:
            timestamps = dataset[loc][1]
            print('Total messages sent to',name,':',len(timestamps))
            day_deltas = [(x-joined_fb).days for x in timestamps]
            freq_data = Counter(day_deltas)
            timelined = [(freq_data[x] if x in freq_data else 0) for x in range(days_since_joining)]
        else:
            raise Exception('Name not found!')
        def rolling_average(dataset,size): # Stolen from gmail data analysis code
            work_from = dataset[size:]
            mean = lambda x: sum(x)/len(x)
            return [mean(dataset[i:i+size]) for i,x in enumerate(work_from)]
        plt.rcParams['figure.figsize'] = (20,10)
        averaged_graphing = rolling_average(timelined,5)
        plt.plot(averaged_graphing)
        if max(averaged_graphing) > largest_max:
            return max(averaged_graphing)
        else:
            return largest_max
    for name in name_list:
        largest_max = subplot(name,dataset,joined_fb,largest_max)
    # Now for context vertical lines
    def context_line(loc,title):
        plt.axvline(loc,c='k')
        plt.text(loc + dx, largest_max,title)
    for event in graph_context:
        context_line((event[0]-joined_fb).days,event[1])
    plt.xlabel('Days since joining Facebook')
    plt.ylabel('Averaged messages in a day')
    plt.legend(name_list)
    plt.savefig('top_msgs_messenger.png')
    plt.show()

# Graph of top message folks
graph_history([y[1] for y in list_names(info)][:graphs[0][1]],info,joined_fb)

### Overall Messenger use frequency
merged_timestamps = []
for i in info:
    merged_timestamps += i[1]
days_since_joining = (datetime.datetime.now()-joined_fb).days
print('Total messages sent:',len(merged_timestamps))
day_deltas = [(x-joined_fb).days for x in merged_timestamps]
freq_data = Counter(day_deltas)
timelined = [(freq_data[x] if x in freq_data else 0) for x in range(days_since_joining)]
def rolling_average(dataset,size): # Stolen from gmail data analysis code
    work_from = dataset[size:]
    mean = lambda x: sum(x)/len(x)
    return [mean(dataset[i:i+size]) for i,x in enumerate(work_from)]
plt.plot(rolling_average(timelined,20))
dx = 10
def context_line(loc,title):
    plt.axvline(loc,c='k')
    plt.text(loc + dx, max(rolling_average(timelined,20)),title)
for event in graph_context:
    context_line((event[0]-joined_fb).days,event[1])
plt.xlabel('Days since joining Facebook')
plt.ylabel('Averaged messages in a day')
plt.savefig('overall_messenger_usage.png')
plt.show()
