

console.log('test');

var a = {{n_reviews}};
console.log(a);

var reviews_rating_pie = c3.generate({
    bindto: '#reviews_rating_pie',
    data: {
        columns: [
            ['a', 30],
            ['b', 120],
            ['c', 30],
            ['d', 120],
            ['e', 120],
        ],
        type : 'pie',
    }
});


var chart = c3.generate({
    bindto: '#chart',
    data: {
      columns: [
        ['users', 30, 200, 100, 400, 150, 250],
        ['products', 50, 20, 10, 40, 15, 25]
      ]
    }
});
