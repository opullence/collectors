from opulence.common.job import Result, StatusCode


def create_result(input=None):
    return Result(input=input, status=StatusCode.empty)
