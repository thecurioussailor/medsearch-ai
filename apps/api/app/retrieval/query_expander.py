class QueryExpander:
    def expand(self, query: str) -> list[str]:
        expansions = {
            "What indicators measure diabetes service delivery?": [
                "What indicators measure diabetes management services?",
                "What indicators assess diabetes care services?",
                "What indicators assess diabetes management and care?",
                "What indicators assess availability of diabetes services?",
            ]
        }

        return expansions.get(query, [query])