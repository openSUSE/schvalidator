#!/bin/bash

if ( [[ $TRAVIS_BRANCH == master ]] || [[ $TRAVIS_BRANCH == develop ]] ); then
    make -C docs deploy
else
    echo "Skipping deploy on '$TRAVIS_BRANCH' branch."
fi
