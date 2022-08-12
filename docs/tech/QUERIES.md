Top content URI
from(bucket: "lens")
|> range(start: -2d)
|> filter(fn: (r) => r["_measurement"] == "INDEXER_COMMENT_CREATED")
|> group(columns: ["contentURI"])
|> aggregateWindow(every: 2d, fn: sum, createEmpty: false)
|> group()
|> sort(columns: ["_value"], desc: true)
|> top(n: 5)


    import "contrib/anaisdg/statsmodels"
    original = from(bucket: "lens")
      |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
      |> filter(fn: (r) => r["_measurement"] == "READ")
      |> filter(fn: (r) => r["_field"] == "READ")
      |> group(columns: ["category"]) // <-- group by application tag
      |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)

    original |> yield(name: "original")

    original
    |> statsmodels.linearRegression()
    |> yield(name: "lr")


    import "contrib/anaisdg/statsmodels"
    original = from(bucket: "bridgeml")
      |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
      |> filter(fn: (r) => r["_measurement"] == "READ")
      |> filter(fn: (r) => r["_field"] == "READ")
      |> group(columns: ["category"])
      |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)

    original |> yield(name: "original")

    original
    |> statsmodels.linearRegression()
    |> map(fn: (r) => ({ r with _value: r.y_hat }))
    |> yield(name: "linreg")
