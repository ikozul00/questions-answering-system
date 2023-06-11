import 'react-native-gesture-handler';
import React from 'react';
import {SafeAreaView, StatusBar} from 'react-native';
import {NavigationContainer} from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';
import {Home} from '../home/Home';
import {ThemeProvider} from 'styled-components/native';
import {ImageDisplay} from '../ImageDisplay/ImageDisplay';
import {Results} from '../Results/Results';
import {ResultDisplay} from '../Results/ResultDisplay';
import {theme} from '../theme/theme';
import {StackParamList} from './types';

const Stack = createStackNavigator<StackParamList>();

export const Screens = function (): JSX.Element {
  return (
    <ThemeProvider theme={theme}>
      <NavigationContainer>
        <SafeAreaView style={{flex: 1}}>
          <StatusBar />
          <Stack.Navigator
            screenOptions={{
              headerStyle: {
                backgroundColor: theme.colors.secondary,
              },
              headerTitleAlign: 'center',
              headerTintColor: theme.colors.tertiary,
              headerTitleStyle: {
                fontWeight: 'bold',
                paddingVertical: 8,
              },
            }}>
            <Stack.Screen name="Home" component={Home} />
            <Stack.Screen
              name="Image"
              component={ImageDisplay}
              initialParams={{uri: ''}}
              options={{title: 'Image'}}
            />
            <Stack.Screen
              name="Results"
              component={Results}
              options={{title: 'Results'}}
            />
            <Stack.Screen
              name="ResultDisplay"
              component={ResultDisplay}
              options={{title: 'Result'}}
              initialParams={{id: ''}}
            />
          </Stack.Navigator>
        </SafeAreaView>
      </NavigationContainer>
    </ThemeProvider>
  );
};
