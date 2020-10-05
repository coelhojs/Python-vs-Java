queries = ["""
query Sprint1 {
    search(query: "stars:>10000 language:{LANG}", type: REPOSITORY, first: 100, {AFTER}) {
        pageInfo {
                hasNextPage
                endCursor
        }
        nodes {
            ... on Repository {
                nameWithOwner
                stargazers {
                    totalCount
                }
                languages(orderBy: {field: SIZE, direction: DESC}, first: 1) {
                    edges {
                        node {
                            name
                        }
                    }
                }
            }
        }
    }
}
"""]
