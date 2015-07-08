import BasePrelude hiding ( always, find )
import Data.HashMap.Strict
import Data.Yaml
import Options.Applicative
import System.FilePath.Find

data Args = Args
  { aSpecsDir :: String
  , aGenDir   :: String
  } deriving ( Eq, Read, Show )

data Package = Package
  { pName :: String
  , pDefs :: [HashMap String Definition]
  } deriving ( Eq, Read, Show )

instance FromJSON Package where
  parseJSON (Object v) = Package <$>
    v .: "package"               <*>
    v .: "definitions"
  parseJSON _ = mzero

data Definition = Definition
  { dId :: Maybe String
  } deriving ( Eq, Read, Show )

instance FromJSON Definition where
  parseJSON (Object v) = Definition <$>
    v .:? "id"
  parseJSON _ = mzero

args :: ParserInfo Args
args =
  info ( helper <*> args' )
    (  fullDesc
    <> header   "gen: Generate Library"
    <> progDesc "Generate Library" ) where
    args' = Args
      <$> strOption
          (  long    "specs-dir"
          <> metavar "DIR"
          <> help    "Specifications Directory" )
      <*> strOption
          (  long    "gen-dir"
          <> metavar "DIR"
          <> help    "Generation Directory" )


getPkgs :: FilePath -> IO [Package]
getPkgs specsDir = do
  specs <- find always (fileName ~~? "*.yaml") specsDir
  pkgs <- forM specs decodeFile
  return $ catMaybes pkgs

exec :: FilePath -> IO ()
exec specsDir = do
  pkgs <- getPkgs specsDir
  print pkgs
  return ()

main :: IO ()
main =
  execParser args >>= call where
    call Args{..} = do
      exec aSpecsDir

