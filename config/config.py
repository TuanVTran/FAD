config = {
  dbURI: 'mongodb://localhost:27017/fad',
  host: 'localhost',
  port: 27017,
  dbName: 'fad',
  alias: 'fad',
  origins: ['*'],
  expires: 30 * 24 * 60 * 60 * 1000,
  rowslimitDefault: 100000,
  dbTimeout: 100000,
  secretKey: 'D@t@lytics.vn',
  oauthPublicKey: 'PKl7wLlml1vCjJ9M_VY-vkLJ_Zo',
  oauthSecretKey: 'DwcOv94EP9zv0hkhZcsJhLkMu7Y',
  awsAccessKeyId: 'AKIAJWDFNPBZXRFVR6SQ',
  awsSecretAccessKey: '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',
  awsBucketName: 'datalytics1',
  awsPrefix: 'MappingFiles',
  intervalCheckFileLoading: 24 * 60 * 60 * 1000
}