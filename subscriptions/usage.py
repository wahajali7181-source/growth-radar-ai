from subscriptions.database import (

    get_feature_usage,

    increase_feature_usage,

    reset_feature_usage

)


def get_usage(

    email,

    feature

):

    return get_feature_usage(

        email,

        feature

    )


def increase_usage(

    email,

    feature

):

    increase_feature_usage(

        email,

        feature

    )


def reset_usage(

    email,

    feature

):

    reset_feature_usage(

        email,

        feature

    )