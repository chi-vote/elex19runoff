import csv, json

### START CONFIG ###
data_dir = '/home/matt/chicago-reporter/elex19runoff/data/'
# infile stuff
precincts_mayoral = 'precinct_canvass_2325.csv'
precincts_mayoral_fieldnames =['ward_precinct',
 '',
 'Registered',
 'Ballots Cast',
 'Turnout (%)',
 '',
 '',
 'LORI LIGHTFOOT',
 'TONI PRECKWINKLE',
 '',
 '',
 'MELISSA CONYEARS-ERVIN',
 'AMEYA PAWAR'] 
precincts_shape_infile = data_dir + 'precincts.json'
# outfiles 
formatted_precincts_outfile_path = data_dir + 'formatted_precincts.json'
precincts_mayoral_outfile_path = data_dir + 'formatted_precinct_canvass.csv'
### END CONFIG ###


def format_precincts_mayoral(infile=open(data_dir+precincts_mayoral)):
    # don't need these header lines
    trunc_data = infile.read().split('\n')[10:]
    # get as csv with custom headers so you can access all fields
    cdata = csv.DictReader(trunc_data,fieldnames=precincts_mayoral_fieldnames)
    # only add real data to the list
    data = [x for x in cdata if 'Ward' in x['ward_precinct'] and 'Precinct' in x['ward_precinct']]
    # here's where we add a ward-precinct code
    wp_data = []
    for datum in data:
        # build a five digi ward-precinct code with approp leading zeroes
        zward = datum['ward_precinct'][5:7].zfill(2)
        zprecinct = datum['ward_precinct'][-2:].zfill(3)
        datum['wp_code'] = zward+zprecinct 
        wp_data.append(datum)
    return wp_data


def write_data(data=format_precincts_mayoral(),outfile=open(precincts_mayoral_outfile_path,'w')):
    complete_fieldnames = [x for x in precincts_mayoral_fieldnames if x]
    fieldnames_w_code = complete_fieldnames + ['wp_code']
    fieldnames_w_code = ['wp_code','Turnout (%)']
    outcsv = csv.DictWriter(outfile,fieldnames=fieldnames_w_code)
    outcsv.writeheader()
    for row in data:
        outcsv.writerow(dict((x,row[x]) for x in row if x in fieldnames_w_code))
    outfile.close()








### DEPRECATED ... SEE readme ###


def format_precincts_json(infile=open(precincts_shape_infile)):
    geojson = json.load(infile)
    counter=0
    for geom in geojson['features']:
        props = geom['properties']
        ward_pct = props['ward'] + '_' + props['precinct']
        geojson['features'][counter]['properties'] = {'ward_pct':ward_pct}
        counter += 1
    return geojson

def write_formatted_geojson(geojson=format_precincts_json(),outfile=open(formatted_precincts_outfile_path,'w')):
    json.dump(geojson,outfile)
    outfile.close()

