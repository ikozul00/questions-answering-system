import React, {useCallback, useEffect, useState} from 'react';
import {View} from 'react-native';
import styled from 'styled-components/native';
// import Icon from 'react-native-vector-icons/FontAwesome5';
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
                <StyledTextLabel key={result.id}>
                  {result.title}
                </StyledTextLabel>
              ))}
            </StyledViewProgress>
          )}
          {done?.length !== 0 && <StyledTextTitle>Done</StyledTextTitle>}
          {done?.map(result => (
            <ResultButton id={result.id} title={result.title} key={result.id} />
          ))}
        </View>
        <StyledTouchableOpacityRefresh onPress={getResults}>
          {/* TODO: find out how to add icon */}
          {/* <Icon name="sync" size={30} color="#900" /> */}
          <StyledTextRefresh>Refresh</StyledTextRefresh>
        </StyledTouchableOpacityRefresh>
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

const StyledTextLabel = styled.Text`
  padding-top: ${({theme}) => theme.spaces.space16};
  color: ${({theme}) => theme.colors.secondary};
  font-size: ${({theme}) => theme.fontSizes.medium};
`;

const StyledTouchableOpacityRefresh = styled.Text`
  margin-right: ${({theme}) => theme.spaces.space16};
`;

const StyledTextRefresh = styled.Text`
  color: ${({theme}) => theme.colors.secondary};
  font-size: ${({theme}) => theme.fontSizes.large};
`;
