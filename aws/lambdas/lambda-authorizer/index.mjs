import { CognitoJwtVerifier } from "aws-jwt-verify";
import { SSMClient, GetParameterCommand } from "@aws-sdk/client-ssm";

const ssm = new SSMClient({});

let verifier; // We'll initialize this lazily after fetching SSM params

export const handler = async (event) => {
  const rawToken = event.headers.authorization || event.headers.Authorization;

  if (!rawToken || !rawToken.startsWith("Bearer ")) {
    console.error("Missing or malformed Authorization header:", rawToken);
    return generateDeny("user", event.routeArn);
  }

  const token = rawToken.split(" ")[1];

  if (!token) {
    return generateDeny("user", event.routeArn);
  }

  try {
    // Lazy init verifier
    if (!verifier) {
      const [userPoolId, clientId] = await Promise.all([
        getSSMParam("/cruddur/cognito/USER_POOL_ID"),
        getSSMParam("/cruddur/cognito/CLIENT_ID"),
      ]);
      verifier = CognitoJwtVerifier.create({
        userPoolId,
        clientId,
        tokenUse: "access",
      });
    }

    const payload = await verifier.verify(token);
    const principalId = payload.sub;

    return generateAllow(principalId, event.routeArn, payload);
  } catch (err) {
    console.error("Token verification failed:", err);
    return generateDeny("user", event.routeArn);
  }
};

async function getSSMParam(name) {
  const cmd = new GetParameterCommand({ Name: name, WithDecryption: true });
  const res = await ssm.send(cmd);
  return res.Parameter.Value;
}

function generateAllow(principalId, resource, payload) {
  return {
    principalId,
    policyDocument: {
      Version: "2012-10-17",
      Statement: [
        {
          Action: "execute-api:Invoke",
          Effect: "Allow",
          Resource: resource,
        },
      ],
    },
    context: payload, // Pass token claims downstream
  };
}

function generateDeny(principalId, resource) {
  return {
    principalId,
    policyDocument: {
      Version: "2012-10-17",
      Statement: [
        {
          Action: "execute-api:Invoke",
          Effect: "Deny",
          Resource: resource,
        },
      ],
    },
  };
}
