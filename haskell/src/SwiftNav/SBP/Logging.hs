-- |
-- Module:      SwiftNav.SBP.Logging
-- Copyright:   Copyright (C) 2015 Swift Navigation, Inc.
-- License:     LGPL-3
-- Maintainer:  Mark Fine <dev@swiftnav.com>
-- Stability:   experimental
-- Portability: portable
--
-- Logging and debugging messages from the device. These are in the
-- implementation-defined range (0x0000-0x00FF).

module SwiftNav.SBP.Logging where

import BasicPrelude
import Control.Monad
import Control.Monad.Loops
import Data.Aeson.TH (deriveJSON, defaultOptions, fieldLabelModifier)
import Data.Binary
import Data.Binary.Get
import Data.Binary.IEEE754
import Data.Binary.Put
import Data.ByteString
import Data.ByteString.Lazy hiding ( ByteString )
import Data.Int
import Data.Word
import SwiftNav.SBP.Encoding

msgLog :: Word16
msgLog = 0x0401

-- | SBP class for message MSG_LOG (0x0401).
--
-- This message contains a human-readable payload string from the device
-- containing errors, warnings and informational messages at ERROR, WARNING,
-- DEBUG, INFO logging levels.
data MsgLog = MsgLog
  { msgLog_level :: Word8
    -- ^ Logging level
  , msgLog_text :: ByteString
    -- ^ Human-readable string
  } deriving ( Show, Read, Eq )

instance Binary MsgLog where
  get = do
    msgLog_level <- getWord8
    msgLog_text <- liftM toStrict getRemainingLazyByteString
    return MsgLog {..}

  put MsgLog {..} = do
    putWord8 msgLog_level
    putByteString msgLog_text

$(deriveJSON defaultOptions {fieldLabelModifier = fromMaybe "msgLog_" . stripPrefix "msgLog_"}
             ''MsgLog)

msgTweet :: Word16
msgTweet = 0x0012

-- | SBP class for message MSG_TWEET (0x0012).
--
-- All the news fit to tweet.
data MsgTweet = MsgTweet
  { msgTweet_tweet :: ByteString
    -- ^ Human-readable string
  } deriving ( Show, Read, Eq )

instance Binary MsgTweet where
  get = do
    msgTweet_tweet <- getByteString 140
    return MsgTweet {..}

  put MsgTweet {..} = do
    putByteString msgTweet_tweet

$(deriveJSON defaultOptions {fieldLabelModifier = fromMaybe "msgTweet_" . stripPrefix "msgTweet_"}
             ''MsgTweet)

msgPrintDep :: Word16
msgPrintDep = 0x0010

-- | SBP class for message MSG_PRINT_DEP (0x0010).
--
-- Deprecated.
data MsgPrintDep = MsgPrintDep
  { msgPrintDep_text :: ByteString
    -- ^ Human-readable string
  } deriving ( Show, Read, Eq )

instance Binary MsgPrintDep where
  get = do
    msgPrintDep_text <- liftM toStrict getRemainingLazyByteString
    return MsgPrintDep {..}

  put MsgPrintDep {..} = do
    putByteString msgPrintDep_text

$(deriveJSON defaultOptions {fieldLabelModifier = fromMaybe "msgPrintDep_" . stripPrefix "msgPrintDep_"}
             ''MsgPrintDep)
