import type {NativeStackNavigationProp} from '@react-navigation/native-stack';
import type {RouteProp} from '@react-navigation/native';

export type StackParamList = {
  Home: undefined;
  Image: {
    file: {
      fileName: string | undefined;
      type: string | undefined;
      uri: string | undefined;
    };
  };
  Results: undefined;
  ResultDisplay: {id: string};
};

export type HomeScreenNavigationProp = NativeStackNavigationProp<
  StackParamList,
  'Home'
>;

export type ImageScreenNavigationProp = NativeStackNavigationProp<
  StackParamList,
  'Image'
>;

export type ResultsScreenNavigationProp = NativeStackNavigationProp<
  StackParamList,
  'Results'
>;

export type ImageScreenRouteProp = RouteProp<StackParamList, 'Image'>;

export type ResultScreenRouteProp = RouteProp<StackParamList, 'ResultDisplay'>;
