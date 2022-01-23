var express = require("express");
var path = require("path");
var logger = require("morgan");
var pug = require("pug");
const mongoose = require("mongoose");
const { MongoClient } = require("mongodb");
var mongo = require("mongodb");
var stringSimilarity = require("string-similarity");
require("dotenv").config();
const port = 5000;

// Atlas connection string
const url = process.env.MONGO_CONNECTION_STRING;
// The database to use
const dbName = "gettingStarted";
//https://docs.atlas.mongodb.com/tutorial/insert-data-into-your-cluster/
const client = new MongoClient(url);

var app = express();
// view engine setup
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "pug");
app.use("/public", express.static(path.join(__dirname, "public")));
app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, "public")));

app.get("/", async function (req, res, next) {
  try {
    res.render("index");
  } catch (err) {
    console.log(err.stack);
  }
});

/* Levenshtein distance 
(amount of string edits to go froam string a to string b for distance)
https://en.wikipedia.org/wiki/Levenshtein_distance */

function editDistance(s1, s2) {
  s1 = s1.toLowerCase();
  s2 = s2.toLowerCase();

  var costs = new Array();
  for (var i = 0; i <= s1.length; i++) {
    var lastValue = i;
    for (var j = 0; j <= s2.length; j++) {
      if (i == 0) costs[j] = j;
      else {
        if (j > 0) {
          var newValue = costs[j - 1];
          if (s1.charAt(i - 1) != s2.charAt(j - 1))
            newValue = Math.min(Math.min(newValue, lastValue), costs[j]) + 1;
          costs[j - 1] = lastValue;
          lastValue = newValue;
        }
      }
    }
    if (i > 0) costs[s2.length] = lastValue;
  }
  return costs[s2.length];
}

function similarity(s1, s2) {
  var longer = s1;
  var shorter = s2;
  if (s1.length < s2.length) {
    longer = s2;
    shorter = s1;
  }
  var longerLength = longer.length;
  if (longerLength == 0) {
    return 1.0;
  }
  return (
    (longerLength - editDistance(longer, shorter)) / parseFloat(longerLength)
  );
}

app.get("/searchquerry", async function (req, res, next) {
  await client.connect();
  console.log("Connected correctly to server");
  const db = client.db(dbName);
  // Use the collection "people"
  const col = db.collection("people");

  console.log(req.query.marke);
  //Model

  console.log(req.query.title);

  //var input = req.query.title
  //var stringArray = input.split(/(\s+)/);
  //console.log(stringArray);

  var query = { title: new RegExp(req.query.title.toLowerCase()) };
  var sort = { title: 1 };
  var data = await col
    .find({ title: { $regex: req.query.title.toLowerCase() } })
    .sort(sort)
    .toArray();

  var händlerlist = [];
  for (i = 0; i < data.length; i++) {
    try {
      console.log(data[i].title);
      if (0.1 <= similarity(data[i].title, req.query.title.toLowerCase())) {
        //if(0.3 <= stringSimilarity.compareTwoStrings(data[i].title, req.query.title.toLowerCase())){
        händlerlist.push(data[i]);
      }
    } catch (error) {
      console.log(error);
    }
  }
  console.log("händlerlist: ", händlerlist);
  if (händlerlist.length === 0) {
    res.render("err");
  } else {
    //console.log("data from query:", data[0].title)
    res.render("list", {
      tabledata: händlerlist,
      searchquery: req.query.title,
    });
  }
});

app.get("/:PRODUCTID", async function (req, res, next) {
  await client.connect();
  console.log("Connected correctly to server");
  const db = client.db(dbName);
  // Use the collection "people"
  const col = db.collection("people");

  console.log(req.params.PRODUCTID);

  var o_id = new mongo.ObjectID(req.params.PRODUCTID);
  var query = { _id: o_id };
  var data = await col.find(query).toArray();

  console.log("current product title:", data[0].title);

  var sort2 = { title: 1 };
  var data2 = await col.find({}).sort(sort2).toArray();

  var händlerlist = [];
  for (i = 0; i < data2.length; i++) {
    try {
      //console.log(data2[i].title);
      //console.log(similarity(data2[i].title, data[0].title.toLowerCase()));
      if (0.78 <= similarity(data2[i].title, data[0].title.toLowerCase())) {
        //if(0.3 <= stringSimilarity.compareTwoStrings(data[i].title, req.query.title.toLowerCase())){
        händlerlist.push(data2[i]);
      }
    } catch (error) {
      console.log(error);
    }
  }
  //console.log("händlerlist: ", händlerlist)

  //for sort by tmp_distances - but also sort similarproducts array at the same time
  function doubleBubbleSort(arr, arr2) {
    for (let j = 0; j < arr.length; j++) {
      for (let i = 0; i < arr.length; i++) {
        if (arr[i] > arr[i + 1]) {
          var temp = arr[i];
          arr[i] = arr[i + 1];
          arr[i + 1] = temp;

          var temp2 = arr2[i];
          arr2[i] = arr2[i + 1];
          arr2[i + 1] = temp2;
        }
      }
    }
    return arr2;
  }

  var similarproducts = [];
  var tmp_distances = [];

  for (i = 0; i < data2.length; i++) {
    try {
      //console.log(data2[i].title);
      //console.log(similarity(data2[i].title, data[0].title.toLowerCase()));
      if (
        0.77 > similarity(data2[i].title, data[0].title.toLowerCase()) &&
        0.5 < similarity(data2[i].title, data[0].title.toLowerCase())
      ) {
        distance = similarity(data2[i].title, data[0].title.toLowerCase());
        tmp_distances.push(distance);
        similarproducts.push(data2[i]);
      }
    } catch (error) {
      console.log(error);
    }
  }

  sorted_data = await doubleBubbleSort(tmp_distances, similarproducts);
  reversed_sorted_data = sorted_data.reverse(); //high to low
  console.log("sorted_data", sorted_data);
  //console.log(sorted_data);
  //console.log("distance", tmp_distances);

  /*
    // filter out prod;ucts with high price distance 
    var filtered_data = [];
    var threshhold = data[0].price * 0.5;
    console.log(threshhold );

    for(i = 0; i < reversed_sorted_data.length; i++ ){
        if(reversed_sorted_data[i].price >= threshhold ){
            filtered_data.push(reversed_sorted_data[i]);
        }
    }
    console.log("filtered_data", filtered_data);
    */

  //console.log("händlerlist: ", similarproducts)
  //console.log("data from query:", data)
  res.render("product", {
    tabledata: data[0],
    new_data: händlerlist,
    similar: reversed_sorted_data,
  });
});

app.listen(process.env.PORT || 5000, () => {
  console.log(`App listening at http://localhost:${port}`);
});
