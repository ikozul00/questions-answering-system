import React, {useCallback, useEffect, useState} from 'react';
import {Text, TouchableOpacity, View} from 'react-native';
import styled from 'styled-components/native';
// import Icon from 'react-native-vector-icons/FontAwesome';
import {ResultButton} from './ResultButton';

interface Result {
  id: string;
  title: string;
}

export const Results = function (): JSX.Element {
  const [inProgress, setInProgress] = useState<Result[]>();
  const [done, setDone] = useState<Result[]>();

  const getResults = useCallback(async () => {
    try {
      //Address of localhost on android emulator: 10.0.2.2
      const response = await fetch(`http://localhost:8000/getResults/`);
      if (!response.ok) {
        console.warn('Problem fetching text.');
        return;
      }
      const jsonRes = await response.json();
      setInProgress(jsonRes.inprogress);
      setDone(jsonRes.done);
    } catch (err) {
      console.warn(err);
    }
  }, []);

  useEffect(() => {
    getResults();
  }, []);

  return (
    <StyledScrollView
      contentContainerStyle={{
        flexGrow: 1,
      }}>
      <StyledViewContainer>
        <View>
          {inProgress?.length !== 0 && (
            <StyledViewProgress>
              <StyledTextTitle>In progress</StyledTextTitle>
              {inProgress?.map(result => (
                <ResultButton
                  id={result.id}
                  title={result.title}
                  key={result.id}
                />
              ))}
            </StyledViewProgress>
          )}
          {done?.length !== 0 && <StyledTextTitle>Done</StyledTextTitle>}
          {done?.map(result => (
            <ResultButton id={result.id} title={result.title} key={result.id} />
          ))}
        </View>
        <TouchableOpacity onPress={getResults}>
          {/* <Icon name="sync" size={30} color="#FFFFFF" /> */}
          <Text>Refresh</Text>
        </TouchableOpacity>
      </StyledViewContainer>
    </StyledScrollView>
  );
};

const StyledScrollView = styled.ScrollView`
  background-color: ${({theme}) => theme.colors.background};
`;

const StyledViewContainer = styled.View`
  margin-top: ${({theme}) => theme.spaces.space16};
  margin-left: ${({theme}) => theme.spaces.space16};
  flex-direction: row;
  justify-content: space-between;
`;

const StyledViewProgress = styled.View`
  margin-bottom: ${({theme}) => theme.spaces.space48};
`;

const StyledTextTitle = styled.Text`
  color: ${({theme}) => theme.colors.primary};
  font-size: ${({theme}) => theme.fontSizes.extralarge};
`;
