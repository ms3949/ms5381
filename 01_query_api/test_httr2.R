#' @name test_httr2.R
#' @title GET request with httr2 (GitHub API)
#' @author Prof. Tim Fraser
#' @description
#' Topic: API queries with httr2
#'
#' Demonstrates how to make a GET request in R using httr2.
#' Fetches the public profile for the GitHub user "octocat".

# 0. SETUP ###################################

## 0.1 Load Packages #################################

library(httr2)  # for HTTP requests (GET, POST, etc.)

# 1. MAKE GET REQUEST ###################################

# Build the request and perform it in one pipeline.
# request(url) creates a request; GET is the default when there is no body.
# req_perform() sends the request and returns the response.
resp = request("https://api.github.com/users/octocat") |>
  req_perform()

# 2. INSPECT RESPONSE ###################################

# HTTP status (200 = success)
resp$status_code

# Response body as parsed JSON (list in R)
resp_body_json(resp)
