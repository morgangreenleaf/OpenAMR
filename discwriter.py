def discwriter(discs, descriptors, filepath, ids, dosages, content):
    # cnx = mysql.connector.connect(user='root', database='incubator', password = 'Letmein!')
    # connect to database
    cursor = dbh.cursor()
    cursor.execute("select abx_name from antibiotics")
    # get names
    discnames = cursor.fetchall()
    cursor.execute("select abx_descriptor from antibiotics")
    # get descriptors
    knownfeatures = cursor.fetchall()

    cursor.execute("select abx_id from antibiotics")
    ids = cursor.fetchall()

    existance = np.zeros(len(discs), np.uint8)
    head, tail = os.path.split(filepath)
    # makes sure all discs are known
    for d in range(0, len(discs)):
        for n in range(0, len(discnames)):
            if (discs[d + 1] == discnames[n]):
                if (knownfeatures[n] != ''):
                    # if a discs name matches one found in the database
                    features = open(knownfeatures[n][0], "wb")
                    pairdisc = pickle.load(features)
                    # access its descriptors
                    pairdisc[len(pairdisc)] = descriptors[d]
                    # open the dictionary and add the new descriptor to it at len(descriptors) since it starts at zero
                    features.close()
                    # close it
                    features = open(knownfeatures[n][0], "wb")
                    # dump it at the same point
                    pickle.dump(pairdisc, features)
                    features.close()
                    existance[d] = 1
                else:
                    entirepath = ''
                    if (len(filepath) > 0):
                        entirepath = head + '/' + discs[d + 1] + '.pkl'
                    # make a file at a given folder
                    else:
                        entirepath = discs[d + 1] + '.pkl'
                    tempdict = {}
                    features = open(entirepath, "wb")
                    tempdict[0] = descriptors[d + 1]
                    # make a new dictionary and dump it in that file
                    pickle.dump(tempdict, features)
                    features.close()
                    cursor.execute("update antibiotics set abx_descriptor = " + entirepath + "where abx_id = " str(abx_id[n]))


                    # record that you found the same path

    for a in range(1, len(discs) + 1):
        if (existance[a - 1] != 1):
            entirepath = ''
            # If you don't find a matching antibiotic
            if (len(filepath) > 0):
                entirepath = head + '/' + discs[a] + '.pkl'
            # make a file at a given folder
            else:
                entirepath = discs[a] + '.pkl'
            # make a pickle file with those descriptors in a dictionary
            tempdict = {}
            features = open(entirepath, "wb")
            tempdict[0] = descriptors[a]
            # make a new dictionary and dump it in that file
            pickle.dump(tempdict, features)
            features.close()
            # push it to the database.
            cursor.execute("insert into `antibiotics`  VALUES (" + str(ids[a]) + ", " + str(discs[a]) + ", " + str(
                content[a]) + ", " + dosages[a] + ", " + entirepath + ")")
