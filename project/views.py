from django.shortcuts import render
import pandas as pd
import numpy as np
import statistics
import seaborn as sns
import matplotlib.pyplot as plt
import json

def index(request):
    df = pd.read_csv('asset/dropdown.csv')
    lists = df['batsman']
    lists2 = df['team'].dropna()
    return render(request , 'index.html', {'list' : lists,'list2':lists2} )

def aboutus(request):

    return render(request,'aboutus.html')

def index2(request):

    return render(request , 'index.html')

def bastmenanalysis(request):
    if request.method == 'POST':
        df = pd.read_csv('asset/deliveries.csv')
        Teams = {
            'Royal Challengers Bangalore': 'RCB',
            'Sunrisers Hyderabad': 'SRH',
            'Rising Pune Supergiant': 'RPS',
            'Mumbai Indians': 'MI',
            'Kolkata Knight Riders': 'KKR',
            'Gujarat Lions': 'GL',
            'Kings XI Punjab': 'KXIP',
            'Delhi Daredevils': 'DD',
            'Chennai Super Kings': 'CSK',
            'Rajasthan Royals': 'RR',
            'Deccan Chargers': 'DC',
            'Kochi Tuskers Kerala': 'KTK',
            'Pune Warriors': 'PW',
            'Rising Pune Supergiants': 'RPS'
        }

        df['batting_team'] = df['batting_team'].map(Teams)
        df['bowling_team'] = df['bowling_team'].map(Teams)
        name = request.POST.get('playername')
        print(name)
        filt = (df['batsman'] == name)
        df_warner = df[filt]

        #Runs vs Teams
        runs_vs_teams = df_warner.groupby(['bowling_team'])['batsman_runs'].sum()
        runs_scored_vs_teams = [['K','V']]
        for x, y in runs_vs_teams.iteritems():
            t = [x, y]
            runs_scored_vs_teams.append(t)
        print(runs_scored_vs_teams)
        runs_scored_vs_teams = json.dumps(runs_scored_vs_teams)


        # Dismissal Kind of Player
        c = df_warner['dismissal_kind'].value_counts()
        k = [['K', 'V']]
        for x, y in c.iteritems():
            t = [x, y]
            k.append(t)
        dis_kind = json.dumps(k)

        # ball wise contribution of player
        one = count(df_warner,1)
        two = count(df_warner,2)
        three = count(df_warner,3)
        four = count(df_warner,4)
        six = count(df_warner,6)
        runs_cont = [['K','V'],['One',one],['Two',two],['Three',three],['Four',four],['Six',six]]
        runs_cont = json.dumps(runs_cont)


        # most wicket taken of while bowling

        filt = (df['bowler'] == name)
        df_bowler = df[filt]
        df_bowler = df_bowler[df_bowler['dismissal_kind'].notnull() == True]
        most_wicket_by_bowler = df_bowler['batsman'].value_counts()
        most_wicket_taken = []
        i = 0
        for x, y in most_wicket_by_bowler.iteritems():
            t = [x, y]
            most_wicket_taken.append(t)
            i = i + 1
            if i > 5:
                break
        most_wicket_taken = json.dumps(most_wicket_taken)

        # Wickets Vs Teams
        wickets_vs_team = df_bowler.groupby(['batting_team'])['is_wicket'].sum()
        wickets_taken_vs_teams = [['K', 'V']]
        for x, y in wickets_vs_team.iteritems():
            t = [x, y]
            wickets_taken_vs_teams.append(t)
        wickets_taken_vs_teams = json.dumps(wickets_taken_vs_teams)

        #Statistics

        # most out by bowlers
        filt = df_warner[df_warner['dismissal_kind'].notnull() == True]
        bowler_taken = filt['bowler'].value_counts()
        most_wicket = []
        i=0
        for x, y in bowler_taken.iteritems():
            t = [x, y]
            most_wicket.append(t)
            i=i+1
            if i>5:
                break
        most_wicket = json.dumps(most_wicket)

        t = json.dumps(name)
        ecom = {'diskind': dis_kind,'runscont':runs_cont, 'name': t, 'most_wic' : most_wicket, 'most_wicket_taken':most_wicket_taken,'runs_vs_teams':runs_scored_vs_teams
                ,'wickets_taken_vs_teams': wickets_taken_vs_teams}
        return render(request, 'bastman.html', ecom)
    ecom = {'k' :10}
    return render(request, 'bastman.html', ecom)

def team(request):
    if request.method == 'POST':
        df = pd.read_csv('asset/deliveries.csv')
        name = request.POST.get('teamname')

        filt = (df['batting_team'] == name)
        df_batting = df[filt]

        Teams = {
            'Royal Challengers Bangalore': 'RCB',
            'Sunrisers Hyderabad': 'SRH',
            'Rising Pune Supergiant': 'RPS',
            'Mumbai Indians': 'MI',
            'Kolkata Knight Riders': 'KKR',
            'Gujarat Lions': 'GL',
            'Kings XI Punjab': 'KXIP',
            'Delhi Daredevils': 'DD',
            'Chennai Super Kings': 'CSK',
            'Rajasthan Royals': 'RR',
            'Deccan Chargers': 'DC',
            'Kochi Tuskers Kerala': 'KTK',
            'Pune Warriors': 'PW',
            'Rising Pune Supergiants': 'RPS'
        }

        df_batting['batting_team'] = df_batting['batting_team'].map(Teams)
        df_batting['bowling_team'] = df_batting['bowling_team'].map(Teams)

        # Runs Scored vs All Teams

        runs_vs_teams = df_batting.groupby(['match_id', 'bowling_team'])['total_runs'].sum()

        K =[]
        for x, y in runs_vs_teams.iteritems():
            t = [x[0],x[1], y]
            K.append(t)
        runs_vs_teams = pd.DataFrame(K,columns=['match_id', 'bowling_team','total'])
        runs_vs_teams2 = runs_vs_teams

        runs_vs_teams = round(runs_vs_teams.groupby(['bowling_team']).mean(),0)
        runs_vs_teams = pd.DataFrame(runs_vs_teams)
        runs_vs_teams.to_csv('asset/abc.csv')
        runs_vs_teams = pd.read_csv('asset/abc.csv')

        a1 = runs_vs_teams['bowling_team'].to_list()
        a2 = runs_vs_teams['total'].to_list()

        k = [['Team Name', 'V']]

        for x, y in zip(a1, a2):
            t = [x, y]
            k.append(t)
        runs_scored_vs_teams = json.dumps(k)

        #highest runs for Team

        highest_runs = df_batting.groupby(['batsman'])['batsman_runs'].sum()
        highest_runs= highest_runs.sort_values(ascending=False)[:10]
        highest_runs_vs_teams = [['K', 'V']]
        for x, y in highest_runs.iteritems():
            t = [x, y]
            highest_runs_vs_teams.append(t)
        highest_runs_vs_teams = json.dumps(highest_runs_vs_teams)

        #boxplot Runs scored vs all teams
        fig, ax = plt.subplots()
        sns.boxplot(x='bowling_team', y='total', data=runs_vs_teams2, ax=ax)
        plt.savefig('asset/box2.png')

        t = json.dumps(name)
        ecom ={'name':t,'runs_scored_vs_teams':runs_scored_vs_teams ,'highest_runs_vs_teams' :highest_runs_vs_teams}
        return render(request, 'team.html',ecom)




def analysis(request):
    df = pd.read_csv('asset/deliveries.csv')
    df_matches = pd.read_csv('asset/matches.csv')

    # score>200 runs agaist batting team
    high_200 = df.groupby(['match_id', 'inning', 'batting_team', 'bowling_team'])['total_runs'].sum().reset_index()

    high_200.set_index(['match_id'], inplace=True)
    highestscore = high_200['total_runs'].max()
    # score more then 200
    high = high_200.rename(columns={'total_runs': 'count'})
    high = high[high['count'] >= 200].groupby(['inning', 'batting_team', 'bowling_team']).count()

    # params = {'more200': val1,'highestscore':highestscore}
    # max runs of player
    max_runs = df.groupby(['batsman'])['batsman_runs'].sum()
    maxrun = max_runs.sort_values(ascending=False)[:10]

    k = [['K', 'V']]
    for x, y in maxrun.iteritems():
        t = [x, y]
        k.append(t)
    max1 = json.dumps(k)

    df['dismissal_kind'].unique()
    dismissal_kinds = ['caught', 'bowled', 'lbw', 'caught and bowled',
                       'stumped', 'hit wicket']
    hwt = df[df["dismissal_kind"].isin(dismissal_kinds)]
    hwt.head()
    highestwicket = hwt['bowler'].value_counts()[:10]
    b = [['K', 'V']]
    for x, y in highestwicket.iteritems():
        t = [x, y]
        b.append(t)
    highestwicket = json.dumps(b)


    #Toss Winning
    toss_win =df_matches['toss_winner'].value_counts().sort_values()
    k = [['K', 'Bar', 'Line']]
    for x, y in toss_win.iteritems():
        t = [x, y,y]
        k.append(t)
    toss_win = json.dumps(k)

    # highest runs for Team

    # runs = df.groupby(['match_id', 'inning', 'batting_team'])[['total_runs']].sum().reset_index()
    # runs.drop('match_id', axis=1, inplace=True)
    # inning1 = runs[runs['inning'] == 1]
    # inning2 = runs[runs['inning'] == 2]

    # highest_runs = highest_runs.sort_values(ascending=False)[:10]
    # highest_runs_vs_teams = [['K', 'V']]
    # for x, y in highest_runs.iteritems():
    #     t = [x, y]
    #     highest_runs_vs_teams.append(t)
    # highest_runs_vs_teams = json.dumps(highest_runs_vs_teams)

    #Most MOM
    most_mom = df_matches['player_of_match'].value_counts()
    k = []
    i =0
    for x, y in most_mom.iteritems():
        t = [x, y]
        k.append(t)
        if i>9:
            break
        i=i+1
    most_mom = json.dumps(k)

    # Total Wins
    matches_played_byteams = pd.concat([df_matches['team1'], df_matches['team2']], axis=1)
    teams = (matches_played_byteams['team1'].value_counts() + matches_played_byteams[
        'team2'].value_counts()).reset_index()
    teams.columns = ['team_name', 'Matches_played']
    matches_played_byteams = pd.concat([df_matches['team1'], df_matches['team2']], axis=1)
    wins = pd.DataFrame(df_matches['winner'].value_counts()).reset_index()
    wins.columns = ['team_name', 'wins']
    player = teams.merge(wins, left_on='team_name', right_on='team_name', how='inner')
    player.columns = ['team', 'matches_played', 'wins']
    player['win_per'] = (player['wins'] / player['matches_played']) * 100
    player = player.iloc[:, [0,3]]

    a1 = player['team'].to_list()
    a2 = player['win_per'].to_list()

    k = [['K', 'V']]

    for x, y in zip(a1,a2):
        t = [x, y]
        k.append(t)
    most_wins = json.dumps(k)

    #runs scored Distribution - boxplot

    Teams = {
        'Royal Challengers Bangalore': 'RCB',
        'Sunrisers Hyderabad': 'SRH',
        'Rising Pune Supergiant': 'RPS',
        'Mumbai Indians': 'MI',
        'Kolkata Knight Riders': 'KKR',
        'Gujarat Lions': 'GL',
        'Kings XI Punjab': 'KXIP',
        'Delhi Daredevils': 'DD',
        'Chennai Super Kings': 'CSK',
        'Rajasthan Royals': 'RR',
        'Deccan Chargers': 'DC',
        'Kochi Tuskers Kerala': 'KTK',
        'Pune Warriors': 'PW',
        'Rising Pune Supergiants': 'RPS'
    }

    df['batting_team'] = df['batting_team'].map(Teams)
    df['bowling_team'] = df['bowling_team'].map(Teams)

    runs = df.groupby(['match_id', 'inning', 'batting_team'])[['total_runs']].sum().reset_index()
    fig, ax = plt.subplots()
    sns.boxplot(x='batting_team', y='total_runs', data=runs, ax=ax)
    plt.savefig('asset/box.png')


    params = {'more': high, 'maxscore': highestscore, 'maxruns': max1, 'highestwicket': highestwicket,'toss_win':toss_win
              ,'most_mom':most_mom, 'most_wins':most_wins ,}

    return render(request, 'analysis.html', params)




def count(df,runs):
    return len(df[df['batsman_runs']==runs])*runs

def timepass(request):
    # runs scored Distribution - boxplot

    # runs = df.groupby(['match_id', 'inning', 'batting_team'])[['total_runs']].sum().reset_index()
    # runs = pd.DataFrame(runs)
    # runs = runs.groupby(['batting_team'])['total_runs'].describe()
    # runs = pd.DataFrame(runs)
    # runs.to_csv('asset/runs.csv')

    runs = pd.read_csv('asset/runs.csv')

    print(runs)
    runs = round(runs)
    batting_team = runs['batting_team'].to_list()
    min = runs['min'].to_list()
    firstQur = runs['25%'].to_list()
    median = runs['50%'].to_list()
    thirdqur = runs['75%'].to_list()
    max = runs['max'].to_list()

    distribution = []

    for z, a, b, c, d, e in zip(batting_team, max, min, firstQur, median, thirdqur):
        t = [z, a, b, c, d, e]
        distribution.append(t)

    # distribution = json.dumps(distribution)


    return render(request, 'timepass.html',{'distribution':distribution})